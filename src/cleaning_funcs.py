import pandas as pd
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def impute_county(df: pd.DataFrame) -> pd.DataFrame:
    """
    Impute missing County values using reverse geocoding from Nominatim.
    Safely handles errors, avoids duplicate geocoding, and reports progress.
    """

    geolocator = Nominatim(user_agent="hospital-dashboard", timeout=5)

    # Filter only rows where County is missing
    df_null = df.loc[df["County"].isna()].copy()

    # Cache so we don't geocode the same coordinates twice
    cache = {}

    print(f"Attempting to fill {len(df_null)} missing counties...\n")

    for index, row in df_null.iterrows():
        lat, lon = row["Latitude"], row["Longitude"]

        # Skip rows with no coordinates
        if pd.isna(lat) or pd.isna(lon):
            print(f"Skipping index {index} (missing coordinates)")
            continue

        coord_key = (lat, lon)

        # Check cache first
        if coord_key in cache:
            df.at[index, "County"] = cache[coord_key]
            print(f"[CACHE] Filled index {index}: {cache[coord_key]}")
            continue

        # Try reverse geocoding
        try:
            location = geolocator.reverse(f"{lat}, {lon}")

            if location and "address" in location.raw:
                county = location.raw["address"].get("county")

                if county:
                    df.at[index, "County"] = county
                    cache[coord_key] = county
                    print(f"[OK] Filled index {index}: {county}")
                else:
                    print(f"[NO COUNTY] Index {index}: No county found")
            else:
                print(f"[NO ADDRESS] Index {index}: no address data")

            # Be polite to API
            time.sleep(1)

        except (GeocoderTimedOut, GeocoderServiceError):
            print(f"[TIMEOUT] Index {index}, skipping…")
            continue

        except Exception as e:
            print(f"[ERROR] Index {index}: {repr(e)}")

    print("\nDone filling counties.")
    return df

def impute_city(df: pd.DataFrame) -> pd.DataFrame:
    """
    Impute missing city values using reverse geocoding from Nominatim.
    Safely handles errors, avoids duplicate geocoding, and reports progress.
    """

    geolocator = Nominatim(user_agent="hospital-dashboard", timeout=5)

    # Filter only rows where City is missing
    df_null = df.loc[df["City"].isna()].copy()

    # Cache so we don't geocode the same coordinates twice
    cache = {}

    print(f"Attempting to fill {len(df_null)} missing cities...\n")

    for index, row in df_null.iterrows():
        lat, lon = row["Latitude"], row["Longitude"]

        # Skip rows with no coordinates
        if pd.isna(lat) or pd.isna(lon):
            print(f"Skipping index {index} (missing coordinates)")
            continue

        coord_key = (lat, lon)

        # Check cache first
        if coord_key in cache:
            df.at[index, "City"] = cache[coord_key]
            print(f"[CACHE] Filled index {index}: {cache[coord_key]}")
            continue

        # Try reverse geocoding
        try:
            location = geolocator.reverse(f"{lat}, {lon}")

            if location and "address" in location.raw:
                city = location.raw["address"].get("city")

                if city:
                    df.at[index, "city"] = city
                    cache[coord_key] = city
                    print(f"[OK] Filled index {index}: {city}")
                else:
                    print(f"[NO CITY] Index {index}: No city found")
            else:
                print(f"[NO ADDRESS] Index {index}: no address data")

            # Be polite to API
            time.sleep(1)

        except (GeocoderTimedOut, GeocoderServiceError):
            print(f"[TIMEOUT] Index {index}, skipping…")
            continue

        except Exception as e:
            print(f"[ERROR] Index {index}: {repr(e)}")

    print("\nDone filling cities.")
    return df
