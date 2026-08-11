"""
Browser control and automation
"""
import subprocess
import time
import webbrowser
from typing import Dict, Optional
from urllib.parse import quote


class BrowserControl:
    """Control browser and web navigation"""
    
    def __init__(self, browser: str = "chrome"):
        self.browser = browser.lower()
    
    def open_website(self, url: str) -> Dict:
        """
        Open a website in default browser
        
        Args:
            url: Website URL
        
        Returns:
            Result dictionary
        """
        try:
            # Add http:// if no protocol specified
            if not url.startswith(('http://', 'https://')):
                url = f"https://{url}"
            
            webbrowser.open(url)
            time.sleep(2)  # Give browser time to load
            
            return {
                "success": True,
                "message": f"Opened {url}",
                "url": url
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error opening website: {str(e)}",
                "error": str(e)
            }
    
    def search_google(self, query: str) -> Dict:
        """
        Search on Google
        
        Args:
            query: Search query
        
        Returns:
            Result dictionary
        """
        try:
            search_url = f"https://www.google.com/search?q={quote(query)}"
            webbrowser.open(search_url)
            time.sleep(2)
            
            return {
                "success": True,
                "message": f"Searched for '{query}'",
                "query": query
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error searching: {str(e)}",
                "error": str(e)
            }
    
    def search_youtube(self, query: str) -> Dict:
        """
        Search on YouTube
        
        Args:
            query: Search query
        
        Returns:
            Result dictionary
        """
        try:
            search_url = f"https://www.youtube.com/results?search_query={quote(query)}"
            webbrowser.open(search_url)
            time.sleep(2)
            
            return {
                "success": True,
                "message": f"Searched YouTube for '{query}'",
                "query": query
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error searching YouTube: {str(e)}",
                "error": str(e)
            }
    
    def open_url(self, url: str) -> Dict:
        """Open any URL"""
        return self.open_website(url)
