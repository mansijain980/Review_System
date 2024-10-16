import os
from django.http import JsonResponse
from django.views import View
from .models import Review
from .serializers import ReviewSerializer
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from firecrawl.firecrawl import FirecrawlApp

class ReviewScraperView(View):
    def get(self, request):
        product_url = request.GET.get('url', None)
        page_number = request.GET.get('pageNumber', '1')  # Default to page 1 if not provided

        # Validate the product_url and reviewerType
        if not product_url:
            return JsonResponse({"error": "No product URL provided"}, status=400)


        # Convert page_number to integer
        try:
            page_number = int(page_number)
        except ValueError:
            return JsonResponse({"error": "Invalid page number provided"}, status=400)

        all_reviews = []  # Store all reviews across pages
        
        try:
            # Retrieve API key from environment variables
            api_key = os.getenv('FIRECRAWL_API_KEY')
            if not api_key:
                return JsonResponse({"error": "Firecrawl API key not found"}, status=500)

            # Initialize Firecrawl with the API key
            firecrawl_app = FirecrawlApp(api_key=api_key)

            # Use Playwright to load the product page
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)

                # Construct the product URL with the requested page number
                page_url = self.construct_pagination_url(product_url, page_number)
                print(f"Fetching URL: {page_url}")  # Debugging: Print the current URL being fetched

                page = browser.new_page()
                page.goto(page_url)

                # Wait for the page to fully load and get the HTML
                page.wait_for_selector('body')
                html_content = page.content()

                # Print the HTML content for debugging
                print(f"HTML Content for Page {page_number}:\n", html_content[:2000])  # First 2000 characters for debugging

                # Parse the HTML using BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')

                # Extract reviews using BeautifulSoup
                review_elements = soup.find_all('div', {'data-hook': 'review'})  # Adjust selector based on actual HTML

                if not review_elements:
                    return JsonResponse({"error": "No reviews found on this page"}, status=404)

                for review in review_elements:
                    title = review.find('a', {'data-hook': 'review-title'}).get_text(strip=True) if review.find('a', {'data-hook': 'review-title'}) else "No Title"
                    body = review.find('span', {'data-hook': 'review-body'}).get_text(strip=True) if review.find('span', {'data-hook': 'review-body'}) else "No Body"
                    
                    # Adjusting the rating extraction to get only the numeric value
                    rating_text = review.find('i', {'data-hook': 'review-star-rating'}).get_text(strip=True) if review.find('i', {'data-hook': 'review-star-rating'}) else "0 stars"
                    # Extract the numeric part of the rating
                    rating = float(rating_text.split(' ')[0]) if 'out' in rating_text else 0.0
                
                    reviewer = review.find('span', class_='a-profile-name').get_text(strip=True) if review.find('span', class_='a-profile-name') else "Anonymous"
                
                    all_reviews.append({
                        'title': title,
                        'body': body,
                        'rating': rating,  # Now this is a float
                        'reviewer': reviewer,
                        'product_url': product_url
                    })

                # Close the browser
                browser.close()

            # Save the reviews to the database (Optional)
            for review_data in all_reviews:
                Review.objects.create(**review_data)

            # Serialize the reviews data for returning the JSON response
            serialized_reviews = ReviewSerializer(all_reviews, many=True).data

            return JsonResponse({
                'reviews_count': len(all_reviews),
                'reviews': serialized_reviews
            }, status=200)

        except Exception as e:
            # Print the error for debugging purposes
            print("Error occurred:", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    def construct_pagination_url(self, base_url, page_number):
        """Constructs the pagination URL based on the base URL and page number."""
        # Ensure we properly encode the URL for use in a request
        base_url = base_url.split('?')[0]  # Get the base URL without query params
        params = base_url.split('/')[4:]  # Extract path after the base URL
        page_query = f"?ie=UTF8&reviewerType=all_reviews&pageNumber={page_number}"
        
        # Rebuild the URL using the correct parameters
        return f"https://www.amazon.in/{'/'.join(params)}{page_query}"

