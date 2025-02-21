import pandas as pd
from urllib.parse import urlparse
from collections import Counter
import math

# Function to calculate entropy (used for domain randomness detection)
def entropy(domain):
    p, _ = Counter(domain).values(), len(domain)
    return -sum(f / _ * math.log2(f / _) for f in p)

# Feature extraction function
def extract_features(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    return {
        "url_length": len(url),
        "num_dots": url.count('.'),
        "has_https": 1 if "https" in url else 0,
        "num_hyphens": url.count('-'),  # Phishing URLs often use hyphens
        "num_digits": sum(c.isdigit() for c in url),  # Many phishing sites use numbers in domains
        "num_special_chars": sum(not c.isalnum() for c in url),  # Counts special characters
        "domain_entropy": entropy(domain),  # Random-looking domains are often phishing
        "subdomain_count": domain.count('.')  # Many phishing URLs use extra subdomains
    }

# Load dataset and apply feature extraction
def load_dataset(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"Dataset loaded successfully with {len(data)} entries.")
        
        # Apply feature extraction to each URL
        data_features = pd.DataFrame(data["url"].apply(extract_features).tolist())
        data_features["label"] = data["label"]  # Add target labels
        
        return data_features
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None
