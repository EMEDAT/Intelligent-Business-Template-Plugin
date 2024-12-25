INDUSTRY_TEMPLATES = {
    "saas": {
        "business_plan": {
            "sections": [
                {
                    "title": "Executive Summary",
                    "subsections": [
                        "Product Overview",
                        "Market Opportunity",
                        "Business Model",
                        "Financial Highlights"
                    ]
                },
                {
                    "title": "Product Description",
                    "subsections": [
                        "Core Features",
                        "Technology Stack",
                        "Product Roadmap",
                        "Development Timeline"
                    ]
                },
                {
                    "title": "Market Analysis",
                    "subsections": [
                        "Target Market Size",
                        "Customer Segments",
                        "Competitor Analysis",
                        "Market Trends"
                    ]
                },
                {
                    "title": "Growth Strategy",
                    "subsections": [
                        "Customer Acquisition",
                        "Pricing Strategy",
                        "Marketing Channels",
                        "Sales Process"
                    ]
                },
                {
                    "title": "Financial Plan",
                    "subsections": [
                        "Revenue Model",
                        "Cost Structure",
                        "Funding Requirements",
                        "Financial Projections"
                    ]
                }
            ]
        }
    },
    "ecommerce": {
        "business_plan": {
            "sections": [
                {
                    "title": "Executive Summary",
                    "subsections": [
                        "Business Concept",
                        "Market Opportunity",
                        "Competitive Advantage",
                        "Financial Overview"
                    ]
                },
                {
                    "title": "Product Strategy",
                    "subsections": [
                        "Product Lines",
                        "Supplier Relations",
                        "Inventory Management",
                        "Quality Control"
                    ]
                },
                {
                    "title": "Market Analysis",
                    "subsections": [
                        "Target Demographics",
                        "Market Size",
                        "Competition",
                        "Industry Trends"
                    ]
                },
                {
                    "title": "Operations Plan",
                    "subsections": [
                        "Fulfillment Process",
                        "Supply Chain",
                        "Customer Service",
                        "Returns Management"
                    ]
                },
                {
                    "title": "Marketing Strategy",
                    "subsections": [
                        "Digital Marketing",
                        "Social Media",
                        "SEO Strategy",
                        "Customer Retention"
                    ]
                }
            ]
        }
    },
    "b2b": {
        "business_plan": {
            "sections": [
                {
                    "title": "Executive Summary",
                    "subsections": [
                        "Company Overview",
                        "Value Proposition",
                        "Market Position",
                        "Growth Strategy"
                    ]
                },
                {
                    "title": "Product/Service Offering",
                    "subsections": [
                        "Core Solutions",
                        "Technical Specifications",
                        "Implementation Process",
                        "Support Services"
                    ]
                },
                {
                    "title": "Market Analysis",
                    "subsections": [
                        "Industry Analysis",
                        "Target Industries",
                        "Buyer Personas",
                        "Competitive Landscape"
                    ]
                },
                {
                    "title": "Sales Strategy",
                    "subsections": [
                        "Sales Process",
                        "Account Management",
                        "Partnership Strategy",
                        "Revenue Model"
                    ]
                },
                {
                    "title": "Operations",
                    "subsections": [
                        "Service Delivery",
                        "Quality Assurance",
                        "Team Structure",
                        "Scalability Plan"
                    ]
                }
            ]
        }
    }
}

def get_template_structure(industry: str, template_type: str) -> dict:
    """
    Get the template structure for a specific industry and template type
    """
    return INDUSTRY_TEMPLATES.get(industry, {}).get(template_type, {})

def get_available_industries() -> list:
    """
    Get a list of available industries
    """
    return list(INDUSTRY_TEMPLATES.keys())

def get_available_templates(industry: str) -> list:
    """
    Get available templates for a specific industry
    """
    return list(INDUSTRY_TEMPLATES.get(industry, {}).keys())