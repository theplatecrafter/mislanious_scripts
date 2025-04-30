slider_data = {
        "Environment & Energy": {
            "color": (50, 200, 50),  # Green
            "sub_categories": {
                "Fossil Fuel Consumption": 70,
                "Carbon Emissions": 75,
                "Air Quality": 60,
                "Global Temperature": 80,
                "Sea Level Rise": 65,
                "Investment in Renewable Energy": 40,
                "Deforestation Rate": 55,
                "Species Biodiversity": 50,
                "Ocean Acidification": 70,
                "Methane Emissions": 65,
                "Plastic Pollution": 80,
                "Water Usage": 75,
                "Renewable Energy Production": 30,
                "Energy Efficiency": 50,
                "Sustainable Agriculture": 40,
            },
        },
        "Economy": {
            "color": (255, 200, 50),  # Yellow
            "sub_categories": {
                "Economic Growth": 60,
                "Unemployment Rate": 40,
                "Global Energy Prices": 70,
                "Income Inequality": 70,
                "Industrial Output": 65,
                "Resource Scarcity": 55,
                "Trade Openness": 75,
                "Inflation Rate": 50,
                "Interest Rates": 45,
                "Stock Market Volatility": 55,
                "Foreign Direct Investment": 60,
            },
        },
        "Society": {
            "color": (50, 100, 255),  # Blue
            "sub_categories": {
                "Population Growth": 60,
                "Urbanization Rate": 55,
                "Healthcare Access": 65,
                "Education Access": 70,
                "Social Stability": 60,
                "Migration Rate": 50,
                "Crime Rate": 40,
                "Civic Participation": 55,
                "Life Expectancy": 75,
                "Public Trust in Institutions": 40,
                "Cultural Diversity": 70,
            },
        },
        "Politics & Governance": {
            "color": (200, 50, 255),  # Magenta
            "sub_categories": {
                "Military Spending": 50,
                "Government Transparency": 45,
                "Democratic Index": 60,
                "Corruption Perception": 65,
                "International Cooperation": 50,
                "Freedom of Press": 60,
                "Political Stability": 65,
                "Rule of Law": 70,
                "Regulatory Quality": 60,
                "Voice and Accountability": 55,
            },
        },
        "Technology & Innovation": {
            "color": (255, 50, 200),  # Pink
            "sub_categories": {
                "Tech Innovation Rate": 70,
                "AI Development": 50,
                "Cybersecurity Investment": 60,
                "Automation Penetration": 55,
                "Space Exploration Funding": 40,
                "Digital Literacy": 65,
                "Internet Access": 75,
                "Renewable Energy Tech": 45,
                "Biotechnology Development": 60,
            },
        },
        "Health & Epidemics": {
            "color": (255, 50, 50),  # Red
            "sub_categories": {
                "Global Pandemic Risk": 80,
                "Vaccination Rate": 70,
                "Antibiotic Resistance": 60,
                "Obesity Rate": 65,
                "Mental Health Index": 50,
                "Access to Clean Water": 75,
            },
        },
        "Agriculture & Food": {
            "color": (100, 255, 100),  # Light Green
            "sub_categories": {
                "Food Security": 60,
                "Crop Yield": 70,
                "Agricultural Land Use": 65,
                "Meat Consumption": 55,
                "Sustainable Farming Practices": 40,
                "Food Waste": 70,
            },
        },
        "Culture & Wellbeing": {
            "color": (200, 200, 200),  # Gray
            "sub_categories": {
                "Mental Health Index": 55,
                "Work-Life Balance": 60,
                "Cultural Diversity": 75,
                "Social Connectedness": 65,
                "Leisure Time": 50,
                "Arts and Culture Funding": 45,
            },
        },
    }




engine.connect_sliders("Fossil Fuel Consumption", "Carbon Emissions", 0.8)
    engine.connect_sliders("Carbon Emissions", "Global Temperature", 0.7)
    engine.connect_sliders("Global Temperature", "Sea Level Rise", 0.6)
    engine.connect_sliders("Investment in Renewable Energy", "Fossil Fuel Consumption", -0.5)
    engine.connect_sliders("Economic Growth", "Unemployment Rate", -0.6)
    engine.connect_sliders("Economic Growth", "Inflation Rate", 0.5)
    engine.connect_sliders("Inflation Rate", "Interest Rates", 0.9)
    engine.connect_sliders("Population Growth", "Urbanization Rate", 0.8)
    engine.connect_sliders("Healthcare Access", "Life Expectancy", 0.7)
    engine.connect_sliders("Education Access", "Digital Literacy", 0.6)
    engine.connect_sliders("Tech Innovation Rate", "Economic Growth", 0.4)
    engine.connect_sliders("AI Development", "Automation Penetration", 0.7)
    engine.connect_sliders("Global Pandemic Risk", "Vaccination Rate", -0.9)
    engine.connect_sliders("Food Security", "Sustainable Farming Practices", 0.6)
    engine.connect_sliders("Mental Health Index", "Social Connectedness", 0.5)
    engine.connect_sliders("Fossil Fuel Consumption", "Global Energy Prices", 0.7)
    engine.connect_sliders("Carbon Emissions", "Air Quality", -0.8)
    engine.connect_sliders("Air Quality", "Healthcare Access", -0.6)
    engine.connect_sliders("Global Temperature", "Agricultural Land Use", -0.5)
    engine.connect_sliders("Sea Level Rise", "Migration Rate", 0.4)
    engine.connect_sliders("Investment in Renewable Energy", "Economic Growth", 0.6)
    engine.connect_sliders("Deforestation Rate", "Species Biodiversity", -0.9)
    engine.connect_sliders("Species Biodiversity", "Food Security", 0.5)
    engine.connect_sliders("Ocean Acidification", "Food Security", -0.4)
    engine.connect_sliders("Methane Emissions", "Global Temperature", 0.6)
    engine.connect_sliders("Plastic Pollution", "Ocean Acidification", 0.7)
    engine.connect_sliders("Water Usage", "Agricultural Land Use", 0.8)
    engine.connect_sliders("Renewable Energy Production", "Global Energy Prices", -0.6)
    engine.connect_sliders("Energy Efficiency", "Fossil Fuel Consumption", -0.4)
    engine.connect_sliders("Sustainable Agriculture", "Food Security", 0.7)
    engine.connect_sliders("Economic Growth", "Industrial Output", 0.8)
    engine.connect_sliders("Unemployment Rate", "Social Stability", -0.7)
    engine.connect_sliders("Global Energy Prices", "Inflation Rate", 0.6)
    engine.connect_sliders("Income Inequality", "Social Stability", -0.9)
    engine.connect_sliders("Industrial Output", "Resource Scarcity", 0.5)
    engine.connect_sliders("Resource Scarcity", "Global Energy Prices", 0.4)
    engine.connect_sliders("Trade Openness", "Economic Growth", 0.6)
    engine.connect_sliders("Inflation Rate", "Income Inequality", -0.5)
    engine.connect_sliders("Interest Rates", "Stock Market Volatility", 0.7)
    engine.connect_sliders("Stock Market Volatility", "Foreign Direct Investment", -0.6)
    engine.connect_sliders("Foreign Direct Investment", "Economic Growth", 0.9)
    engine.connect_sliders("Population Growth", "Food Security", -0.4)
    engine.connect_sliders("Urbanization Rate", "Air Quality", -0.5)
    engine.connect_sliders("Healthcare Access", "Economic Growth", 0.4)
    engine.connect_sliders("Education Access", "Income Inequality", -0.6)
    engine.connect_sliders("Social Stability", "Migration Rate", -0.5)
    engine.connect_sliders("Migration Rate", "Social Stability", -0.4)
    engine.connect_sliders("Crime Rate", "Social Stability", -0.8)
    engine.connect_sliders("Civic Participation", "Government Transparency", 0.7)
    engine.connect_sliders("Life Expectancy", "Healthcare Access", 0.8)
    engine.connect_sliders("Public Trust in Institutions", "Government Transparency", 0.9)
    engine.connect_sliders("Cultural Diversity", "Social Stability", 0.6)
    engine.connect_sliders("Military Spending", "Economic Growth", -0.5)
    engine.connect_sliders("Government Transparency", "Corruption Perception", -0.9)
    engine.connect_sliders("Democratic Index", "Social Stability", 0.7)
    engine.connect_sliders("Corruption Perception", "Foreign Direct Investment", -0.6)
    engine.connect_sliders("International Cooperation", "Global Temperature", -0.4)
    engine.connect_sliders("Freedom of Press", "Government Transparency", 0.8)
    engine.connect_sliders("Political Stability", "Economic Growth", 0.6)
    engine.connect_sliders("Rule of Law", "Foreign Direct Investment", 0.7)
    engine.connect_sliders("Regulatory Quality", "Industrial Output", 0.5)
    engine.connect_sliders("Voice and Accountability", "Social Stability", 0.4)
    engine.connect_sliders("Tech Innovation Rate", "Industrial Output", 0.7)
    engine.connect_sliders("AI Development", "Unemployment Rate", 0.6)
    engine.connect_sliders("Cybersecurity Investment", "Tech Innovation Rate", 0.5)
    engine.connect_sliders("Automation Penetration", "Unemployment Rate", 0.8)
    engine.connect_sliders("Space Exploration Funding", "Tech Innovation Rate", 0.4)
    engine.connect_sliders("Digital Literacy", "Education Access", 0.9)
    engine.connect_sliders("Internet Access", "Digital Literacy", 0.7)
    engine.connect_sliders("Renewable Energy Tech", "Investment in Renewable Energy", 0.6)
    engine.connect_sliders("Biotechnology Development", "Life Expectancy", 0.5)
    engine.connect_sliders("Global Pandemic Risk", "Economic Growth", -0.7)
    engine.connect_sliders("Vaccination Rate", "Life Expectancy", 0.9)
    engine.connect_sliders("Antibiotic Resistance", "Healthcare Access", -0.6)
    engine.connect_sliders("Obesity Rate", "Life Expectancy", -0.5)
    engine.connect_sliders("Mental Health Index", "Social Stability", 0.7)
    engine.connect_sliders("Access to Clean Water", "Healthcare Access", 0.8)
    engine.connect_sliders("Food Security", "Social Stability", 0.6)
    engine.connect_sliders("Crop Yield", "Food Security", 0.8)
    engine.connect_sliders("Agricultural Land Use", "Deforestation Rate", 0.7)
    engine.connect_sliders("Meat Consumption", "Agricultural Land Use", 0.5)
    engine.connect_sliders("Sustainable Farming Practices", "Crop Yield", 0.9)
    engine.connect_sliders("Food Waste", "Food Security", -0.4)
    engine.connect_sliders("Work-Life Balance", "Mental Health Index", 0.7)
    engine.connect_sliders("Social Connectedness", "Mental Health Index", 0.8)
    engine.connect_sliders("Leisure Time", "Work-Life Balance", 0.6)
    engine.connect_sliders("Arts and Culture Funding", "Social Connectedness", 0.5)
    engine.connect_sliders("Air Quality", "Global Temperature", 0.4)
    engine.connect_sliders("Migration Rate", "Population Growth", 0.3)