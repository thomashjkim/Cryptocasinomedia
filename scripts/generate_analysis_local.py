import sys, os, json, random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from update_articles import articles_data

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
JSON_FILE = os.path.join(DATA_DIR, "expert_analysis.json")

templates = [
    (
        "The latest development from {source} signals a crucial shift in the {region} iGaming market. With increased attention on {topic1} and {topic2}, this move serves as a leading indicator of broader market consolidation. Operators and B2B stakeholders must recognize that early adoption of these frameworks is no longer optional, but a baseline requirement for maintaining market share.",
        "From a structural standpoint, integrating {topic1} at this scale forces competing platforms to re-evaluate their compliance and user acquisition models. As {source} establishes this new standard, we expect to see a ripple effect across the Web3 ecosystem, driving up the cost of entry for unlicensed competitors while rewarding platforms with transparent infrastructures."
    ),
    (
        "As the regulatory landscape tightens across {region}, {source}'s recent strategic rollout underscores the growing convergence between traditional finance and crypto-native gambling. By prioritizing {topic1}, the platform is effectively future-proofing its operations against impending KYC/AML mandates that are expected to reshape the industry later this year.",
        "For investors and market analysts, the key takeaway is the focus on {topic2}. Moving away from high-friction legacy systems allows {source} to capture a higher lifetime value (LTV) from VIP segments. This operational efficiency will likely become the blueprint for tier-1 crypto casinos heading into the next fiscal quarter."
    ),
    (
        "This announcement from {source} highlights a rapidly accelerating trend within the global crypto casino sector: the aggressive scaling of {topic1}. While retail attention often focuses on promotional value, the underlying B2B significance here is the robust technological infrastructure required to support {topic2} seamlessly across multiple jurisdictions.",
        "Market dynamics in {region} dictate that user retention is heavily reliant on instant liquidity and provable fairness. By cementing its position in {topic1}, {source} is not just acquiring users—it is acquiring structural trust. Competing entities will need to match this level of transparency or risk severe player attrition."
    ),
    (
        "At the intersection of {topic1} and Web3 innovation, {source} is demonstrating exactly how tier-1 operators are navigating the complex {region} market. The strategic emphasis on {topic2} is a calculated move to attract high-net-worth crypto players who demand institutional-grade security alongside their gaming experience.",
        "What makes this particularly relevant for the broader iGaming industry is the operational pivot. {source} is proving that decentralized infrastructure and regulatory compliance are not mutually exclusive. This approach effectively lowers payment processing overhead while simultaneously elevating the brand's trustworthiness in a crowded marketplace."
    ),
    (
        "The deployment of {topic1} initiatives by {source} represents a maturation of the crypto gambling vertical in {region}. Historically, the sector has struggled with the friction between {topic2} and user experience. This latest update bridges that gap, offering a frictionless environment that appeals to both crypto-natives and traditional bettors.",
        "From an industry analysis perspective, this is a clear defensive moat. By locking in advanced capabilities around {topic1}, {source} mitigates the risk of regulatory backlash while capturing a highly engaged demographic. Other B2B suppliers and operators should view this as a benchmark for the upcoming regulatory cycles."
    )
]

def generate_local_analysis(article):
    source = article.get('sourceName', 'the operator')
    region = article.get('region', 'Global')
    topics = article.get('topics', ['Web3', 'Crypto Casinos'])
    topic1 = topics[0] if len(topics) > 0 else 'Web3 integration'
    topic2 = topics[1] if len(topics) > 1 else 'blockchain compliance'
    
    t1, t2 = random.choice(templates)
    
    p1 = t1.format(source=source, region=region, topic1=topic1, topic2=topic2)
    p2 = t2.format(source=source, region=region, topic1=topic1, topic2=topic2)
    
    return f"{p1}\n\n{p2}"

def main():
    analysis_data = {}
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            analysis_data = json.load(f)
            
    new_count = 0
    for article in articles_data:
        slug = article['slug']
        if slug not in analysis_data:
            analysis_data[slug] = generate_local_analysis(article)
            new_count += 1
            
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(analysis_data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully generated {new_count} expert analyses locally without API!")

if __name__ == "__main__":
    main()
