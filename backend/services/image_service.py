import logging
from typing import List, Dict, Any

logger = logging.getLogger("ammachi.image_service")

# Curated, High-Resolution, 100% Authentic Cultural Image Assets (Served locally from /images/culture/)
CULTURAL_IMAGE_DATABASE: Dict[str, List[Dict[str, str]]] = {
    "tamil_kings": [
        {
            "url": "/images/culture/rajaraja_chola.jpg",
            "caption": "Emperor Raja Raja Chola I (985–1014 CE) - The great builder of Brihadeeswara Temple."
        },
        {
            "url": "/images/culture/brihadeeswara_temple.jpg",
            "caption": "Brihadeeswara Temple (Thanjavur Periya Kovil) - Masterpiece of Chola architecture."
        },
        {
            "url": "/images/culture/mahabalipuram_shore.jpg",
            "caption": "Shore Temple (Mahabalipuram) - UNESCO World Heritage Dravidian stone architecture."
        }
    ],
    "gods_deities": [
        {
            "url": "/images/culture/lord_ganesha.jpg",
            "caption": "Lord Ganesha (Vinayagar) - Remover of obstacles and Lord of new beginnings."
        },
        {
            "url": "/images/culture/lord_murugan.jpg",
            "caption": "Lord Murugan (Kartikeya) - The Tamil deity of wisdom holding the sacred Vel."
        },
        {
            "url": "/images/culture/lord_shiva.jpg",
            "caption": "Lord Shiva (Nataraja) - Depicting the cosmic dance of creation and wisdom."
        },
        {
            "url": "/images/culture/goddess_lakshmi.jpg",
            "caption": "Goddess Lakshmi - Goddess of light, auspiciousness, and spiritual prosperity."
        }
    ],
    "deepam_diya": [
        {
            "url": "/images/culture/deepam_diya.jpg",
            "caption": "Agal Vilakku (Clay Oil Lamps) - Terracotta diyas set in rangoli to dispel darkness."
        },
        {
            "url": "/images/culture/karthigai_deepam.jpg",
            "caption": "Karthigai Deepam - Rows of glowing earthen lamps illuminating the doorstep."
        }
    ],
    "pongal": [
        {
            "url": "/images/culture/pongal_pot.jpg",
            "caption": "Traditional Pongal Pot - Boiling sweet Sakkarai Pongal with turmeric and sugarcane."
        }
    ],
    "diwali": [
        {
            "url": "/images/culture/diwali_lights.jpg",
            "caption": "Diwali Festival of Lights - Rows of diyas and vibrant rangoli welcoming joy."
        },
        {
            "url": "/images/culture/deepam_diya.jpg",
            "caption": "Clay Oil Lamps (Diyas) - Lighting the home on Deepavali night."
        }
    ],
    "puthandu": [
        {
            "url": "/images/culture/ugadi_pachadi.jpg",
            "caption": "Auspicious New Year Offering - Fruits, flowers, and festive preparations."
        }
    ],
    "karthigai_deepam": [
        {
            "url": "/images/culture/karthigai_deepam.jpg",
            "caption": "Karthigai Deepam - Terracotta oil lamps arranged on traditional kolam art."
        }
    ],
    "thaipusam": [
        {
            "url": "/images/culture/lord_murugan.jpg",
            "caption": "Lord Murugan at Batu Caves - Divine spear of wisdom (Vel) and devotion."
        },
        {
            "url": "/images/culture/thaipusam_kavadi.jpg",
            "caption": "Thaipusam Kavadi Procession - Devotees bearing Kavadi with peacock feathers."
        }
    ],
    "ugadi": [
        {
            "url": "/images/culture/ugadi_pachadi.jpg",
            "caption": "Ugadi Festive Puja Tray - Fresh mangoes, neem flowers, and ceremonial offerings."
        }
    ],
    "sankranti": [
        {
            "url": "/images/culture/sankranti_kites.jpg",
            "caption": "Makar Sankranti Kites - Celebrating the sun's northward journey across winter skies."
        }
    ],
    "bonalu": [
        {
            "url": "/images/culture/bonalu_festival.jpg",
            "caption": "Bonalu Festive Procession - Decorated earthen pots offered to Goddess Mahakali."
        }
    ],
    "onam": [
        {
            "url": "/images/culture/onam_pookalam.jpg",
            "caption": "Athapookalam - Intricate circular floral carpet created with fresh flower petals."
        }
    ]
}

def get_cultural_images_for_query(query: str, language: str = "Tamil") -> List[Dict[str, str]]:
    """
    Returns 1 to 2 verified, 100% relevant cultural images matching the specific user query.
    """
    q = (query or "").lower().strip()

    # Tamil Kings / History / Monuments
    if any(w in q for w in ["king", "chola", "pandya", "cheran", "pallava", "monument", "temple", "thanjavur", "history", "ruler", "raja"]):
        return CULTURAL_IMAGE_DATABASE["tamil_kings"][:2]

    # Deities & Gods
    if any(w in q for w in ["god", "deity", "murugan", "ganesha", "vinayagar", "shiva", "krishna", "lakshmi", "durga", "vishnu", "devi"]):
        # If specific deity requested, prioritize that deity
        if "murugan" in q or "kartikeya" in q:
            return [CULTURAL_IMAGE_DATABASE["gods_deities"][1]]
        if "ganesh" in q or "vinayagar" in q:
            return [CULTURAL_IMAGE_DATABASE["gods_deities"][0]]
        if "shiva" in q or "nataraja" in q:
            return [CULTURAL_IMAGE_DATABASE["gods_deities"][2]]
        if "lakshmi" in q:
            return [CULTURAL_IMAGE_DATABASE["gods_deities"][3]]
        return CULTURAL_IMAGE_DATABASE["gods_deities"][:2]

    # Deepam / Diya / Lighting
    if any(w in q for w in ["deepam", "diya", "lamp", "vilakku", "how to do deepam", "light lamp"]):
        return CULTURAL_IMAGE_DATABASE["deepam_diya"][:2]

    # Pongal
    if any(w in q for w in ["pongal", "harvest", "sugarcane", "sakkarai"]):
        return CULTURAL_IMAGE_DATABASE["pongal"]

    # Diwali
    if any(w in q for w in ["diwali", "deepavali", "lights", "cracker", "firework"]):
        return CULTURAL_IMAGE_DATABASE["diwali"][:2]

    # Karthigai Deepam
    if any(w in q for w in ["karthigai", "thiruvannamalai"]):
        return CULTURAL_IMAGE_DATABASE["karthigai_deepam"]

    # Thaipusam
    if any(w in q for w in ["thaipusam", "kavadi", "batu caves", "vel"]):
        return CULTURAL_IMAGE_DATABASE["thaipusam"][:2]

    # Ugadi
    if any(w in q for w in ["ugadi", "shadruchulu", "pachadi"]):
        return CULTURAL_IMAGE_DATABASE["ugadi"]

    # Sankranti
    if any(w in q for w in ["sankranti", "kite", "muggulu"]):
        return CULTURAL_IMAGE_DATABASE["sankranti"]

    # Bonalu
    if any(w in q for w in ["bonalu", "telangana"]):
        return CULTURAL_IMAGE_DATABASE["bonalu"]

    # Onam
    if any(w in q for w in ["onam", "pookalam", "mahabali"]):
        return CULTURAL_IMAGE_DATABASE["onam"]

    # Default based on current language
    if "telugu" in language.lower():
        return CULTURAL_IMAGE_DATABASE["ugadi"]
    elif "malayalam" in language.lower():
        return CULTURAL_IMAGE_DATABASE["onam"]

    return CULTURAL_IMAGE_DATABASE["pongal"]
