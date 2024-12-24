# pages/Liégois.py

import streamlit as st
import http.client
import json
import os
import time
from datetime import datetime
import pytz  # Ensure pytz is installed
import re

# Constants
CACHE_FILE = "static/data/standard_liege_cache.json"
CACHE_DURATION_SECONDS = 86400  # 24 hours
API_HOST = "free-api-live-football-data.p.rapidapi.com"
API_KEY = st.secrets["rapidapi_key"]
STANDARD_TEAM_ID = 9985
BELGIAN_PRO_LEAGUE_ID = 40  # Typically the correct league ID for the Belgian Pro League
STANDARD_TEAM_NAME = "Standard Liege"

# Provided team detail JSON (as a string)
DEFAULT_TEAM_DETAIL_JSON = json.dumps({
    "status": "success",
    "response": {
        "details": {
            "id": 9985,
            "type": "team",
            "name": "Standard Liege",
            "latestSeason": "2024/2025",
            "shortName": "Standard Liege",
            "country": "BEL",
            "faqJSONLD": {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "When is Standard Liege's next match?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Standard Liege's next match is at 17:30 GMT on Thu, 26 Dec 2024 against KV Mechelen."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "Who is Standard Liege's top scorer?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Andi Zeqiri has scored the most goals for Standard Liege, with 6 goals."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "Who is Standard Liege's best player?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Matthieu Epolo is the top-rated player for Standard Liege with a FotMob rating of 7.38."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "Who has the most assists for Standard Liege?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Andi Zeqiri has the most assists on Standard Liege, with 2 assists."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "Where is Standard Liege's stadium?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Standard Liege stadium is located in Liège (Luik) and is called Stade Maurice Dufrasne."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "What is the capacity of Stade Maurice Dufrasne?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "The capacity for Stade Maurice Dufrasne is 27670."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "When was Stade Maurice Dufrasne opened?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Stade Maurice Dufrasne opened in 1909."
                        }
                    }
                ]
            },
            "sportsTeamJSONLD": {
                "@context": "https://schema.org",
                "@type": "SportsTeam",
                "name": "Standard Liege",
                "sport": "Football/Soccer",
                "gender": "https://schema.org/Male",
                "logo": "https://images.fotmob.com/image_resources/logo/teamlogo/9985.png",
                "url": "https://www.fotmob.com/teams/9985/overview/standard-liege",
                "athlete": [],
                "location": {
                    "@type": "Place",
                    "name": "Stade Maurice Dufrasne",
                    "address": {
                        "@type": "PostalAddress",
                        "addressCountry": "Belgium",
                        "addressLocality": "Liège (Luik)"
                    },
                    "geo": {
                        "@type": "GeoCoordinates",
                        "latitude": "50.609893",
                        "longitude": "5.543343"
                    }
                },
                "memberOf": {
                    "@type": "SportsOrganization",
                    "name": "Belgian Pro League",
                    "url": "https://www.fotmob.com/leagues/40/overview/belgian-pro-league"
                }
            },
            "breadcrumbJSONLD": {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": "https://www.fotmob.com"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Belgian Pro League",
                        "item": "https://www.fotmob.com/leagues/40/overview/belgian-pro-league"
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": "Standard Liege",
                        "item": "https://www.fotmob.com/teams/9985/overview/standard-liege"
                    }
                ]
            },
            "canSyncCalendar": True,
            "primaryLeagueId": 40,
            "primaryLeagueName": "Belgian Pro League"
        }
    }
})

# Default fixtures JSON (as a string)
DEFAULT_LEAGUE_MATCHES_JSON = json.dumps({
    "status": "success",
    "response": {
        "fixtures": [
            {
                "date": "2024-12-26T17:30:00.000Z",
                "homeTeamName": "Standard Liege",
                "awayTeamName": "KV Mechelen"
            },
            {
                "date": "2025-01-11T19:45:00.000Z",
                "homeTeamName": "Standard Liege",
                "awayTeamName": "Kortrijk"
            },
            {
                "date": "2025-01-18T17:30:00.000Z",
                "homeTeamName": "St.Truiden",
                "awayTeamName": "Standard Liege"
            },
            {
                "date": "2025-01-25T12:30:00.000Z",
                "homeTeamName": "Standard Liege",
                "awayTeamName": "FCV Dender EH"
            },
            {
                "date": "2025-02-01T17:15:00.000Z",
                "homeTeamName": "Cercle Brugge",
                "awayTeamName": "Standard Liege"
            }
        ]
    }
})

def main():
    st.set_page_config(
        page_title="Standard de Liège",
        page_icon=":soccer:",
        layout="wide"
    )
    
    st.markdown("<h1 style='color: red; text-align: center;'>STANDARD DE LIÈGE</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Bienvenue chez les Rouches! 🦁</h2>", unsafe_allow_html=True)
    
    st.write("___")
    st.write("## :red_circle: Allez Standard! :white_circle:")
    st.write(
        """
        Welcome, fellow **Standard** hooligan. 
        Here you can find the upcoming matches, and all the latest news about our beloved **Standard de Liège**.  
        Grab your beer, bind your scarf around your mouth, and let's cook into the action!  
        """
    )
    st.write("___")
    
    # Manual refresh
    # if st.button("🔄 Refresh Data"):
    #     reset_cache()
    #     st.rerun()
    
    data = get_standard_cache()
    
    display_next_match_info(data)
    display_upcoming_fixtures(data)
    
    st.write("## 🎫 Buy Tickets")
    st.markdown("[Buy your tickets here](https://standard.be/fr/ticketing/equipeA)")
    
    display_team_faq(data)
    display_team_news(data)
    
    st.write("## 🏟️ Official Websites & More")
    st.markdown("[Standard de Liège Official Site](https://standard.be/)")
    st.markdown("[Standard de Liège on FotMob](https://www.fotmob.com/teams/9985/overview/standard-liege)")
    
def get_standard_cache():
    """
    Reads the local JSON cache for Standard data if it exists and is fresh (less than 24h old).
    Otherwise, fetches new data from the free-api-live-football-data and writes it to cache.
    """
    if os.path.isfile(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            try:
                cached_data = json.load(f)
            except json.JSONDecodeError:
                cached_data = {}
        if "timestamp" in cached_data:
            last_updated = cached_data["timestamp"]
            if (time.time() - last_updated) < CACHE_DURATION_SECONDS:
                return cached_data  # still valid

    st.info("Fetching fresh data for Standard de Liège...")
    
    # Team detail
    team_detail_raw = fetch_team_detail(STANDARD_TEAM_ID)
    team_detail_parsed = parse_api_response(team_detail_raw, 'team_detail')
    
    # League matches
    league_matches_raw = fetch_league_matches(BELGIAN_PRO_LEAGUE_ID)
    league_matches_parsed = parse_api_response(league_matches_raw, 'league_matches')
    
    # League news (pages 1,4,7)
    league_news_raw = fetch_league_news(BELGIAN_PRO_LEAGUE_ID, pages=[1])
    league_news_parsed = parse_api_response(league_news_raw, 'league_news')
    
    # Fallback to defaults if needed
    if team_detail_parsed.get("status") != "success":
        st.warning("API call for team detail failed. Using default data.")
        team_detail_parsed = json.loads(DEFAULT_TEAM_DETAIL_JSON)
    
    if league_matches_parsed.get("status") != "success":
        st.warning("API call for league matches failed. Using default fixtures.")
        league_matches_parsed = json.loads(DEFAULT_LEAGUE_MATCHES_JSON)
    
    if league_news_parsed.get("status") != "success":
        st.warning("API call for league news failed. No news will be displayed.")
        league_news_parsed = {"status": "success", "response": {"news": []}}
    
    # Filter news containing "Standard" in the title (case-insensitive)
    # Also remove duplicates by article ID or title
    seen_article_ids = set()
    filtered_news = []
    for article in league_news_parsed.get("response", {}).get("news", []):
        article_id = article.get("id", "")
        title = article.get("title", "").lower()
        
        if "standard" in title and article_id not in seen_article_ids:
            filtered_news.append(article)
            seen_article_ids.add(article_id)
    
    new_data = {
        "timestamp": time.time(),
        "team_detail_raw": json.dumps(team_detail_parsed),
        "league_matches_raw": json.dumps(league_matches_parsed),
        "league_news_raw": json.dumps(filtered_news),
    }
    
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
    
    return new_data

def fetch_team_detail(team_id):
    conn = http.client.HTTPSConnection(API_HOST)
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': API_HOST
    }
    endpoint = f"/football-league-team?teamid={team_id}"
    conn.request("GET", endpoint, headers=headers)
    res = conn.getresponse()
    return res.read().decode("utf-8")

def fetch_league_matches(league_id):
    conn = http.client.HTTPSConnection(API_HOST)
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': API_HOST
    }
    endpoint = f"/football-get-all-matches-by-league?leagueid={league_id}"
    conn.request("GET", endpoint, headers=headers)
    res = conn.getresponse()
    return res.read().decode("utf-8")

def fetch_league_news(league_id, pages=[1, 4, 7]):
    """
    Aggregates news from the specified pages, removing duplicates will be handled later.
    """
    conn = http.client.HTTPSConnection(API_HOST)
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': API_HOST
    }
    
    aggregated_news = []
    for page in pages:
        endpoint = f"/football-get-league-news?leagueid={league_id}&page={page}"
        conn.request("GET", endpoint, headers=headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        try:
            response_json = json.loads(data)
            if response_json.get("status") == "success":
                news_items = response_json.get("response", {}).get("news", [])
                aggregated_news.extend(news_items)
            else:
                st.error(f"API call for league news page {page} failed: {response_json.get('message', '')}")
        except json.JSONDecodeError:
            st.error(f"Failed to parse league news JSON for page {page}.")
    
    return json.dumps({"status": "success", "response": {"news": aggregated_news}})

def parse_api_response(response_text, response_type):
    """
    Parses the API response and returns a dictionary.
    """
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        st.error(f"Failed to parse {response_type} JSON.")
        return {"status": "failed", "message": "Request Failed Please try Again"}

def display_next_match_info(cached_data):
    st.write("## 🏆 Next Match Info")
    raw_team_detail = cached_data.get("team_detail_raw", "")
    if not raw_team_detail:
        st.warning("No team detail data found.")
        return

    try:
        detail_dict = json.loads(raw_team_detail)
        response = detail_dict.get("response", {})
        details = response.get("details", {})
        faq = details.get("faqJSONLD", {})
        main_entities = faq.get("mainEntity", [])
        
        next_match_answer = None
        for item in main_entities:
            question = item.get("name", "")
            if "when is standard liege" in question.lower():
                next_match_answer = item.get("acceptedAnswer", {}).get("text")
                break

        if next_match_answer:
            # Attempt to convert time from GMT -> CET
            match = re.search(r'at (\d{2}:\d{2}) GMT on (.+) against', next_match_answer)
            if match:
                time_str = match.group(1)
                date_str = match.group(2)
                datetime_str = f"{date_str} {time_str}"
                try:
                    gmt_time = datetime.strptime(datetime_str, "%a, %d %b %Y %H:%M")
                    gmt_timezone = pytz.timezone("GMT")
                    gmt_time = gmt_timezone.localize(gmt_time)
                    
                    belgium_timezone = pytz.timezone("Europe/Brussels")
                    belgium_time = gmt_time.astimezone(belgium_timezone)
                    
                    formatted_time = belgium_time.strftime("%A, %d %B %Y at %H:%M CET")
                except ValueError:
                    formatted_time = datetime_str + " CET"
                
                adjusted_answer = next_match_answer.replace(
                    match.group(1) + " GMT on " + match.group(2),
                    formatted_time
                )
                st.markdown(f"**{adjusted_answer}**")
            else:
                st.markdown(f"**{next_match_answer}** (Time conversion failed)")
        else:
            st.write("Couldn't find the next match details in the FAQ JSON.")

    except json.JSONDecodeError:
        st.error("Failed to parse team detail JSON.")

def display_upcoming_fixtures(cached_data):
    st.write("## 📅 Upcoming Game Days")
    raw_league_data = cached_data.get("league_matches_raw", "")
    if not raw_league_data:
        st.warning("No league match data found.")
        return

    try:
        matches_dict = json.loads(raw_league_data)
        fixtures = matches_dict.get("response", {}).get("fixtures", [])

        standard_matches = []
        for fixt in fixtures:
            # If numeric team IDs exist, match by ID
            home_id = fixt.get("homeTeamId")
            away_id = fixt.get("awayTeamId")
            
            # Otherwise, fallback to matching by name
            home_name = fixt.get("homeTeamName", "")
            away_name = fixt.get("awayTeamName", "")

            # If we have numeric IDs, check those
            if home_id is not None and away_id is not None:
                if home_id == STANDARD_TEAM_ID or away_id == STANDARD_TEAM_ID:
                    standard_matches.append(fixt)
            else:
                # Fallback: check if either home or away name is "Standard Liege"
                if STANDARD_TEAM_NAME in (home_name, away_name):
                    standard_matches.append(fixt)

        if not standard_matches:
            st.write("No upcoming fixtures found for Standard de Liège in this data.")
            return

        # Sort by date
        standard_matches_sorted = sorted(standard_matches, key=lambda x: x.get("date", ""), reverse=False)

        for fixture in standard_matches_sorted[:5]:
            date_str = fixture.get("date", "Unknown date")
            home_team = fixture.get("homeTeamName", "???")
            away_team = fixture.get("awayTeamName", "???")
            try:
                gmt_time = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                gmt_timezone = pytz.timezone("GMT")
                gmt_time = gmt_timezone.localize(gmt_time)

                belgium_timezone = pytz.timezone("Europe/Brussels")
                belgium_time = gmt_time.astimezone(belgium_timezone)

                formatted_time = belgium_time.strftime("%A, %d %B %Y at %H:%M CET")
            except ValueError:
                formatted_time = date_str + " CET"
            
            st.markdown(f"**{formatted_time}:** {home_team} vs {away_team}")

    except json.JSONDecodeError:
        st.error("Failed to parse league matches JSON.")

def display_team_faq(cached_data):
    st.write("## ❓ Team FAQ")
    raw_team_detail = cached_data.get("team_detail_raw", "")
    if not raw_team_detail:
        st.warning("No team detail data found.")
        return

    try:
        detail_dict = json.loads(raw_team_detail)
        response = detail_dict.get("response", {})
        details = response.get("details", {})
        faq = details.get("faqJSONLD", {})
        main_entities = faq.get("mainEntity", [])

        if not main_entities:
            st.write("No FAQ data found in the team details.")
            return

        for item in main_entities:
            question = item.get("name", "")
            answer = item.get("acceptedAnswer", {}).get("text", "")
            if question and answer:
                st.markdown(f"**Q: {question}**")
                st.markdown(f"*A: {answer}*")
                st.write("---")
    except json.JSONDecodeError:
        st.error("Failed to parse team detail JSON.")

def display_team_news(cached_data):
    st.write("## 📰 Latest News")
    raw_news = cached_data.get("league_news_raw", "")
    if not raw_news:
        st.warning("No league news data found.")
        return

    try:
        articles = json.loads(raw_news)
        if not articles:
            st.write("No news found for Standard de Liège.")
            return

        # Show up to 5
        for article in articles[:5]:
            title = article.get("title", "No title")
            snippet = article.get("snippet", "...")
            link = article.get("page", {}).get("url", "#")
            image_url = article.get("imageUrl", "")
            st.markdown(f"**{title}**")
            if image_url:
                st.image(image_url, width=200)
            #st.markdown(f"_{snippet}_")
            st.markdown(f'<a href="{link}" target="_blank">Read more</a>', unsafe_allow_html=True)
            # st.write("---")
    except json.JSONDecodeError:
        st.error("Failed to parse league news JSON.")

def reset_cache():
    if os.path.isfile(CACHE_FILE):
        os.remove(CACHE_FILE)
        st.success("Cache reset. Fresh data will be fetched on next load.")
    else:
        st.warning("No cache file found to reset.")

if __name__ == "__main__":
    main()
