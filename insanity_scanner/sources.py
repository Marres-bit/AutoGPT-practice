"""
Sources de contenus insolites
Scrapers pour Reddit, YouTube, Twitter, faits divers
"""
import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict
from abc import ABC, abstractmethod
import random

from .config import GEISConfig


class BaseSource(ABC):
    """Classe de base pour toutes les sources"""
    
    def __init__(self, config: GEISConfig):
        self.config = config
        self.logger = logging.getLogger(f"GEIS.{self.__class__.__name__}")
    
    @abstractmethod
    def fetch(self) -> List[Dict]:
        """Récupère les contenus de la source"""
        pass
    
    def _get_headers(self) -> Dict[str, str]:
        """Headers HTTP avec User-Agent aléatoire"""
        return {
            'User-Agent': random.choice(self.config.user_agents)
        }


class RedditSource(BaseSource):
    """Source Reddit (subreddits insolites)"""
    
    SUBREDDITS = [
        "WTF",
        "PublicFreakout", 
        "CrazyFuckingVideos",
        "AbruptChaos",
        "Unexpected",
        "WinStupidPrizes",
        "instant_regret",
        "ThatsInsane",
        "Damnthatsinteresting",
        "nextfuckinglevel"
    ]
    
    def fetch(self) -> List[Dict]:
        """Fetch depuis Reddit API"""
        items = []
        
        # Si pas de credentials, utiliser API publique limitée
        if not self.config.reddit_client_id:
            self.logger.warning("Pas de credentials Reddit - utilisation API publique")
            return self._fetch_public()
        
        try:
            import praw
            reddit = praw.Reddit(
                client_id=self.config.reddit_client_id,
                client_secret=self.config.reddit_client_secret,
                user_agent=self.config.reddit_user_agent
            )
            
            for subreddit_name in self.SUBREDDITS:
                try:
                    subreddit = reddit.subreddit(subreddit_name)
                    
                    # Top posts de la semaine
                    for post in subreddit.hot(limit=20):
                        # Filtrer par âge
                        post_age_days = (datetime.now() - datetime.fromtimestamp(post.created_utc)).days
                        if post_age_days > self.config.max_content_age_days:
                            continue
                        
                        item = {
                            'id': f"reddit_{post.id}",
                            'source': 'reddit',
                            'subreddit': subreddit_name,
                            'title': post.title,
                            'description': post.selftext[:500] if post.selftext else "",
                            'url': f"https://reddit.com{post.permalink}",
                            'score': post.score,
                            'num_comments': post.num_comments,
                            'created_utc': post.created_utc,
                            'media_url': post.url if post.url.endswith(('.jpg', '.png', '.gif', '.mp4')) else None,
                            'is_video': post.is_video,
                            'upvote_ratio': post.upvote_ratio
                        }
                        items.append(item)
                except Exception as e:
                    self.logger.error(f"Erreur subreddit {subreddit_name}: {e}")
        
        except ImportError:
            self.logger.warning("praw non installé - utilisation API publique")
            return self._fetch_public()
        except Exception as e:
            self.logger.error(f"Erreur Reddit API: {e}")
        
        return items
    
    def _fetch_public(self) -> List[Dict]:
        """Fallback sur l'API publique Reddit (limitée)"""
        items = []
        
        for subreddit_name in self.SUBREDDITS[:3]:  # Limiter pour éviter rate limit
            try:
                url = f"https://www.reddit.com/r/{subreddit_name}/hot.json?limit=10"
                response = requests.get(url, headers=self._get_headers(), timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    for post_data in data['data']['children']:
                        post = post_data['data']
                        
                        item = {
                            'id': f"reddit_{post['id']}",
                            'source': 'reddit',
                            'subreddit': subreddit_name,
                            'title': post['title'],
                            'description': post.get('selftext', '')[:500],
                            'url': f"https://reddit.com{post['permalink']}",
                            'score': post.get('score', 0),
                            'num_comments': post.get('num_comments', 0),
                            'created_utc': post['created_utc'],
                            'media_url': post.get('url') if post.get('url', '').endswith(('.jpg', '.png', '.gif')) else None,
                            'is_video': post.get('is_video', False),
                            'upvote_ratio': post.get('upvote_ratio', 0.5)
                        }
                        items.append(item)
            except Exception as e:
                self.logger.error(f"Erreur fetch public {subreddit_name}: {e}")
        
        return items


class YouTubeSource(BaseSource):
    """Source YouTube (vidéos virales insolites)"""
    
    SEARCH_QUERIES = [
        "shocking moment caught on camera",
        "unbelievable video",
        "crazy incident",
        "bizarre accident",
        "wtf moment",
        "insane footage"
    ]
    
    def fetch(self) -> List[Dict]:
        """Fetch depuis YouTube API"""
        items = []
        
        if not self.config.youtube_api_key:
            self.logger.warning("Pas de clé API YouTube")
            return items
        
        try:
            for query in self.SEARCH_QUERIES[:2]:  # Limiter pour économiser quota
                url = "https://www.googleapis.com/youtube/v3/search"
                params = {
                    'part': 'snippet',
                    'q': query,
                    'type': 'video',
                    'order': 'viewCount',
                    'maxResults': 10,
                    'key': self.config.youtube_api_key,
                    'publishedAfter': (datetime.now() - timedelta(days=self.config.max_content_age_days)).isoformat() + 'Z'
                }
                
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    for video in data.get('items', []):
                        snippet = video['snippet']
                        video_id = video['id']['videoId']
                        
                        item = {
                            'id': f"youtube_{video_id}",
                            'source': 'youtube',
                            'title': snippet['title'],
                            'description': snippet['description'][:500],
                            'url': f"https://www.youtube.com/watch?v={video_id}",
                            'thumbnail_url': snippet['thumbnails']['high']['url'],
                            'channel': snippet['channelTitle'],
                            'published_at': snippet['publishedAt']
                        }
                        items.append(item)
        except Exception as e:
            self.logger.error(f"Erreur YouTube API: {e}")
        
        return items


class TwitterSource(BaseSource):
    """Source Twitter/X (tweets viraux)"""
    
    SEARCH_QUERIES = [
        "#WTF",
        "#shocking",
        "#viral",
        "#insane",
        "#unbelievable"
    ]
    
    def fetch(self) -> List[Dict]:
        """Fetch depuis Twitter API v2"""
        items = []
        
        if not self.config.twitter_bearer_token:
            self.logger.warning("Pas de token Twitter")
            return items
        
        try:
            headers = {
                'Authorization': f'Bearer {self.config.twitter_bearer_token}'
            }
            
            for query in self.SEARCH_QUERIES[:2]:
                url = "https://api.twitter.com/2/tweets/search/recent"
                params = {
                    'query': f"{query} has:media -is:retweet",
                    'max_results': 20,
                    'tweet.fields': 'created_at,public_metrics',
                    'expansions': 'attachments.media_keys',
                    'media.fields': 'url,preview_image_url'
                }
                
                response = requests.get(url, headers=headers, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for tweet in data.get('data', []):
                        metrics = tweet.get('public_metrics', {})
                        
                        item = {
                            'id': f"twitter_{tweet['id']}",
                            'source': 'twitter',
                            'title': tweet['text'][:100],
                            'description': tweet['text'],
                            'url': f"https://twitter.com/i/status/{tweet['id']}",
                            'likes': metrics.get('like_count', 0),
                            'retweets': metrics.get('retweet_count', 0),
                            'replies': metrics.get('reply_count', 0),
                            'created_at': tweet.get('created_at')
                        }
                        items.append(item)
        except Exception as e:
            self.logger.error(f"Erreur Twitter API: {e}")
        
        return items


class FaitsDiversSource(BaseSource):
    """Source faits divers (sites d'actualité insolite)"""
    
    SITES = [
        "https://www.demotivateur.fr/article/insolite",
        "https://www.legorafi.fr/"
    ]
    
    def fetch(self) -> List[Dict]:
        """Scraping de sites de faits divers"""
        items = []
        
        # Note: Implémentation simplifiée
        # En production, utiliser BeautifulSoup + parsing HTML
        self.logger.warning("FaitsDiversSource nécessite BeautifulSoup (non implémenté)")
        
        return items
