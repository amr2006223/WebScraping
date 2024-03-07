import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

class ImageScraper:
    def get_image_links(self,search_query):
        # Construct the URL for Google Images search with the given query
        search_url = f"https://www.google.com/search?q={search_query}&tbm=isch"

        # Set headers to pretend like a web browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Send a request to the search URL
        response = requests.get(search_url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the response
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find image tags in the HTML with a specific class
            img_tags = soup.find_all('img', class_='rg_i Q4LuWd')

            # Collect image links
            image_links = []
            
            # Loop through the found image tags
            for img_tag in img_tags:
                # Get the image source from 'data-src' or 'src'
                data_src = img_tag.get('data-src')
                src = img_tag.get('src')

                # If 'data-src' exists, use it; otherwise, use 'src'
                if data_src:
                    image_links.append({'query': search_query, 'image_link': unquote(data_src)})
                elif src and src.startswith('data:image/jpeg;'):
                    image_links.append({'query': search_query, 'image_link': unquote(src)})
                if len(image_links) == 1:
                     break
            # Return the list of image links
            return image_links
        else:
            # Print an error message if the request was not successful
            print(f"Failed to retrieve images. Status code: {response.status_code}")
            return []
