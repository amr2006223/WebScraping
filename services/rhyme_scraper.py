import requests
from bs4 import BeautifulSoup

class RhymeScraper:
    def fetch_rhymes(self,word):
        # The website we're using to find rhymes
        base_url = "https://www.rhymezone.com"

        # Construct the URL to search for rhymes for the provided word
        search_url = f"{base_url}/r/rhyme.cgi?Word={word}&org1=syl&org2=l&org3=y&typeofrhyme=perfect"

        # Make a request to the website to get the information
        response = requests.get(search_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the information we got from the website
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all the words on the website that are rhymes
            rhyme_elements = soup.find_all('a', class_='r')

            # Try to get specific rhymes, or just take the first three if those don't exist
            specific_indices = [3, 10, 15]
            rhymes = [rhyme.text for i, rhyme in enumerate(rhyme_elements) if i in specific_indices]

            # If no specific rhymes, take the first three
            if not rhymes:
                rhymes = [rhyme.text for i, rhyme in enumerate(rhyme_elements) if i < 3]

            # Give back the list of rhymes
            return rhymes
        else:
            # If something went wrong with the website request, don't give any rhymes
            return None
