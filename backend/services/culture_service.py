import logging
from typing import List, Dict, Any, Optional
from services.youtube_service import get_festival_youtube_videos, search_youtube_api

logger = logging.getLogger("ammachi.culture")

FESTIVALS_DATA = [
    # Tamil Festivals
    {
        "id": "pongal",
        "name": "Pongal",
        "native_name": "பொங்கல்",
        "language": "Tamil",
        "icon": "🌾",
        "summary": "The 4-day Tamil harvest thanksgiving festival dedicated to Surya Bhagavan and farm animals.",
        "significance": "Celebrates prosperity, boiling sweet Pongal pot ('Pongalo Pongal!'), and thanking cattle on Mattu Pongal.",
        "image_url": "/images/culture/pongal_pot.jpg"
    },
    {
        "id": "puthandu",
        "name": "Puthandu (Tamil New Year)",
        "native_name": "புத்தாண்டு",
        "language": "Tamil",
        "icon": "🥭",
        "summary": "Tamil New Year celebrating the first day of the Chithirai month.",
        "significance": "Families make Maanga Pachadi (sweet, sour, bitter tastes representing life's diverse experiences) and view Kanni.",
        "image_url": "/images/culture/ugadi_pachadi.jpg"
    },
    {
        "id": "karthigai_deepam",
        "name": "Karthigai Deepam",
        "native_name": "கார்த்திகை தீபம்",
        "language": "Tamil",
        "icon": "🪔",
        "summary": "The ancient Tamil Festival of Lights celebrated on the full moon day of Karthigai month.",
        "significance": "Rows of clay oil lamps (agal vilakku) are lit to welcome light, wisdom, and joy.",
        "image_url": "/images/culture/karthigai_deepam.jpg"
    },
    {
        "id": "thaipusam",
        "name": "Thaipusam",
        "native_name": "தைப்பூசம்",
        "language": "Tamil",
        "icon": "🦚",
        "summary": "Celebration honoring Lord Murugan receiving the Vel (spear of wisdom).",
        "significance": "Devotees carry Kavadi and yellow flowers symbolizing devotion and courage.",
        "image_url": "/images/culture/thaipusam_kavadi.jpg"
    },
    {
        "id": "vinayagar_chaturthi",
        "name": "Vinayagar Chaturthi",
        "native_name": "விநாயகர் சதுர்த்தி",
        "language": "Tamil",
        "icon": "🐘",
        "summary": "Joyful celebration honoring Lord Vinayagar (Pillaiyar), the remover of all obstacles and giver of wisdom.",
        "significance": "Moulding clay Pillaiyar idols, offering sweet Kozhukattai, Sundal, Arugampul grass, and singing 'Pillaiyare Perumane'.",
        "image_url": "/images/culture/lord_ganesha.jpg"
    },
    {
        "id": "ayudha_pooja",
        "name": "Ayudha Pooja & Saraswathi Pooja",
        "native_name": "ஆயுத பூஜை & சரஸ்வதி பூஜை",
        "language": "Tamil",
        "icon": "📚",
        "summary": "Sacred Navratri celebration honoring Goddess Saraswathi and blessing books, tools, vehicles, and instruments.",
        "significance": "Applying sandal and kumkumam to tools & vehicles, placing books before Goddess Saraswathi, and sharing sweet Pori Kadalai.",
        "image_url": "/images/culture/goddess_lakshmi.jpg"
    },

    # Telugu Festivals
    {
        "id": "ugadi",
        "name": "Ugadi",
        "native_name": "ఉగాది",
        "language": "Telugu",
        "icon": "🌿",
        "summary": "Telugu New Year marking the beginning of a new astronomical cycle.",
        "significance": "Eating Ugadi Pachadi combining 6 flavors (Shadruchulu) symbolizing life's diverse emotions.",
        "image_url": "/images/culture/ugadi_pachadi.jpg"
    },
    {
        "id": "sankranti",
        "name": "Makara Sankranti",
        "native_name": "సంక్రాంతి",
        "language": "Telugu",
        "icon": "🪁",
        "summary": "Telugu harvest festival celebrated with colorful rangoli (Muggulu), kite flying, and Haridasu songs.",
        "significance": "Honors farmers, sun transit, and sweet Ariselu delicacy.",
        "image_url": "/images/culture/sankranti_kites.jpg"
    },
    {
        "id": "bonalu",
        "name": "Bonalu",
        "native_name": "బోనాలు",
        "language": "Telugu",
        "icon": "🏺",
        "summary": "Telangana traditional festival thanking Goddess Mahakali.",
        "significance": "Women carry decorated earthen pots with cooked rice and neem leaves on their heads with joyful folk dances.",
        "image_url": "/images/culture/bonalu_festival.jpg"
    },

    # Malayalam Festivals
    {
        "id": "onam",
        "name": "Onam",
        "native_name": "ഓണം",
        "language": "Malayalam",
        "icon": "🌸",
        "summary": "Grand harvest festival of Kerala welcoming King Mahabali.",
        "significance": "Creating intricate flower carpets (Pookalam), boat races (Vallamkali), and grand Onasadya feast.",
        "image_url": "/images/culture/onam_pookalam.jpg"
    },

    # Hindi Cultural Festivals
    {
        "id": "holi",
        "name": "Holi (Festival of Colors)",
        "native_name": "होली",
        "language": "Hindi",
        "icon": "🎨",
        "summary": "The vibrant Festival of Colors celebrating spring, friendship, and the victory of Bhakt Prahlad.",
        "significance": "Playing with organic Gulal, lighting the Holika Dahan bonfire, sharing sweet Gujiya, and forgiving past grudges.",
        "image_url": "/images/culture/diwali_lights.jpg"
    },
    {
        "id": "dussehra",
        "name": "Dussehra (Vijayadashami)",
        "native_name": "दशहरा / विजयादशमी",
        "language": "Hindi",
        "icon": "🏹",
        "summary": "Triumph of Lord Rama over the 10-headed demon king Ravana and Goddess Durga over Mahishasura.",
        "significance": "Watching vibrant Ramlila plays, burning giant effigies of Ravana, and starting auspicious new learning.",
        "image_url": "/images/culture/deepam_diya.jpg"
    },
    {
        "id": "raksha_bandhan",
        "name": "Raksha Bandhan",
        "native_name": "रक्षाबंधन",
        "language": "Hindi",
        "icon": "🧵",
        "summary": "Sacred festival celebrating the eternal bond of love, care, and protection between brothers and sisters.",
        "significance": "Sisters tie the sacred Rakhi thread on brothers' wrists with Tilak, sharing sweets and promises of mutual care.",
        "image_url": "/images/culture/deepam_diya.jpg"
    },
    {
        "id": "janmashtami",
        "name": "Krishna Janmashtami",
        "native_name": "श्रीकृष्ण जन्माष्टमी",
        "language": "Hindi",
        "icon": "🦚",
        "summary": "Joyful celebration of the birth of Lord Krishna, the eighth avatar of Lord Vishnu in Mathura.",
        "significance": "Midnight temple celebrations, rocking Bal Gopal's swing (Jhula), singing bhajans, and Dahi Handi human pyramids.",
        "image_url": "/images/culture/lord_ganesha.jpg"
    },
    {
        "id": "navratri",
        "name": "Navratri & Durga Puja",
        "native_name": "नवरात्रि",
        "language": "Hindi",
        "icon": "🌸",
        "summary": "Nine sacred nights worshipping the nine divine forms of Goddess Durga (Navadurga).",
        "significance": "Dancing energetic Garba and Dandiya Raas, fasting, traditional colorful attire, and Kanya Pujan on Ashtami/Navami.",
        "image_url": "/images/culture/goddess_lakshmi.jpg"
    },
    {
        "id": "makar_sankranti",
        "name": "Makar Sankranti & Lohri",
        "native_name": "मकर संक्रांति / लोहड़ी",
        "language": "Hindi",
        "icon": "🪁",
        "summary": "Auspicious winter harvest festival marking the Sun's transition into Capricorn (Makara Rashi).",
        "significance": "Flying colorful kites, singing around the Lohri harvest bonfire, and sharing sweet Til-Gud laddoos.",
        "image_url": "/images/culture/sankranti_kites.jpg"
    },
    {
        "id": "ganesh_chaturthi",
        "name": "Ganesh Chaturthi",
        "native_name": "गणेश चतुर्थी",
        "language": "Hindi",
        "icon": "🐘",
        "summary": "Grand celebration welcoming Lord Ganesha, the remover of all obstacles and Lord of wisdom.",
        "significance": "Installing eco-friendly clay Ganesha idols, offering 21 sweet Modaks, chanting 'Ganpati Bappa Morya', and Visarjan.",
        "image_url": "/images/culture/lord_ganesha.jpg"
    },
    {
        "id": "chhath_puja",
        "name": "Chhath Puja",
        "native_name": "छठ पूजा",
        "language": "Hindi",
        "icon": "🌅",
        "summary": "Ancient Vedic thanksgiving festival dedicated to Surya Dev (Sun God) and Chhathi Maiya.",
        "significance": "Offering Arghya standing in holy river waters at sunset and sunrise and baking sweet wheat Thekua.",
        "image_url": "/images/culture/deepam_diya.jpg"
    },

    # Pan-Indian Festivals
    {
        "id": "diwali",
        "name": "Diwali / Deepavali",
        "native_name": "தீபாவளி / दीपावली / దీపావళి",
        "language": "All",
        "icon": "🪔",
        "summary": "The festival of lights celebrating the triumph of light over darkness and good over evil.",
        "significance": "Wearing new clothes, lighting lamps, enjoying homemade sweets, and sharing joy with loved ones.",
        "image_url": "/images/culture/diwali_lights.jpg"
    }
]

# Comprehensive 10 Contextual Questions for Every Festival
FESTIVALS_QUIZ_DATA: Dict[str, List[Dict[str, Any]]] = {
    # ------------------ TAMIL FESTIVALS ------------------
    "pongal": [
        {
            "id": "p1",
            "question": "What phrase do people joyfully shout when the sweet milk boils over the earthen pot during Pongal?",
            "options": ["Pongalo Pongal!", "Happy New Year!", "Jai Ho!", "Vanakkam Amma!"],
            "answer_index": 0,
            "explanation": "When the milk boils over the pot, everyone cheers 'Pongalo Pongal!' to celebrate abundance and prosperity."
        },
        {
            "id": "p2",
            "question": "How many days is the traditional Pongal festival celebrated?",
            "options": ["1 Day", "2 Days", "4 Days", "7 Days"],
            "answer_index": 2,
            "explanation": "Pongal is celebrated across 4 days: Bhogi, Surya Pongal, Mattu Pongal, and Kaanum Pongal."
        },
        {
            "id": "p3",
            "question": "On Bhogi (Day 1 of Pongal), what do families traditionally do?",
            "options": ["Fly kites", "Clean the house and burn old unwanted items in a morning bonfire", "Fast all day", "Paint bull horns"],
            "answer_index": 1,
            "explanation": "Bhogi marks new beginnings by cleaning homes and discarding old negativity into a bonfire."
        },
        {
            "id": "p4",
            "question": "To which supreme natural deity is the main day of Pongal (Surya Pongal) dedicated?",
            "options": ["Surya Bhagavan (The Sun God)", "Varuna (Rain God)", "Agni (Fire God)", "Vayu (Wind God)"],
            "answer_index": 0,
            "explanation": "Surya Pongal is dedicated to the Sun God for bestowing warmth, energy, and a bountiful harvest."
        },
        {
            "id": "p5",
            "question": "What special animal is lovingly worshipped, bathed, and decorated on Mattu Pongal (Day 3)?",
            "options": ["Elephants", "Farm Cattle (Cows and Bulls)", "Peacocks", "Horses"],
            "answer_index": 1,
            "explanation": "Mattu Pongal honors cattle who work tirelessly in the agricultural fields helping farmers."
        },
        {
            "id": "p6",
            "question": "What sweet ingredients are cooked with freshly harvested rice in the Pongal pot?",
            "options": ["Jaggery (Vellam), Ghee, Cashews & Cardamom", "White Sugar and Chocolate", "Strawberries and Milk", "Honey and Salt"],
            "answer_index": 0,
            "explanation": "Sakkarai Pongal is cooked with fragrant new rice, jaggery, ghee, roasted cashews, and cardamom."
        },
        {
            "id": "p7",
            "question": "What plant stalks are tied around the neck of the Pongal cooking pot as an auspicious symbol?",
            "options": ["Turmeric and Ginger leaves", "Rose stems", "Neem branches", "Banana peel"],
            "answer_index": 0,
            "explanation": "Fresh green turmeric plant leaves (Manjal Kothu) are tied around the pot for auspicious health."
        },
        {
            "id": "p8",
            "question": "What traditional floor art made with rice flour decorates front courtyards during Pongal?",
            "options": ["Kolam (Rangoli)", "Canvas Oil Painting", "Mosaic Tiles", "Clay Sculptures"],
            "answer_index": 0,
            "explanation": "Intricate geometric Kolams made with white rice flour welcome prosperity and feed tiny birds and ants."
        },
        {
            "id": "p9",
            "question": "What sweet tall crop is chewed and enjoyed by children as a symbol of joy on Pongal?",
            "options": ["Sugarcane (Karumbu)", "Bamboo", "Sweet Corn", "Wheat Grass"],
            "answer_index": 0,
            "explanation": "Fresh purple sugarcane stalks (Karumbu) are a delicious festive treat enjoyed on Pongal."
        },
        {
            "id": "p10",
            "question": "What is the final day of Pongal (Kaanum Pongal) primarily celebrated for?",
            "options": ["Family reunions, visiting elders, and enjoying picnics", "Planting new trees", "Total silence and fasting", "Exam preparation"],
            "answer_index": 0,
            "explanation": "Kaanum Pongal brings extended families together for reunions, picnics on riverbanks, and seeking blessings."
        }
    ],
    "puthandu": [
        {
            "id": "pu1",
            "question": "On which Tamil month does Puthandu (Tamil New Year) always occur?",
            "options": ["Chithirai (Mid-April)", "Margazhi (December)", "Aadi (July)", "Thai (January)"],
            "answer_index": 0,
            "explanation": "Puthandu celebrates the first day of the Chithirai month, marking the start of the Tamil solar calendar."
        },
        {
            "id": "pu2",
            "question": "What special dish containing 6 distinct tastes is prepared on Puthandu?",
            "options": ["Maanga Pachadi", "Sakkarai Pongal", "Sambar Rice", "Rasam Vada"],
            "answer_index": 0,
            "explanation": "Maanga Pachadi blends raw mango (sour), jaggery (sweet), neem flowers (bitter), and chilies (spicy)."
        },
        {
            "id": "pu3",
            "question": "What is the philosophical meaning of tasting bitter neem flowers and sweet jaggery in Maanga Pachadi?",
            "options": ["Life is a mixture of joy, challenges, and surprises to be welcomed equally", "Neem is simply colorful", "It is for cold weather", "It was invented by accident"],
            "answer_index": 0,
            "explanation": "The 6 flavors symbolize that life brings diverse moments of happiness and lessons, all to be embraced with grace."
        },
        {
            "id": "pu4",
            "question": "What is the auspicious first sight viewed in the morning mirror on Puthandu called?",
            "options": ["Kanni (Viewing auspicious fruits, flowers, gold, and mirror)", "Deepam", "Aarti", "Kolam"],
            "answer_index": 0,
            "explanation": "Viewing the 'Kanni' tray filled with mangoes, jackfruit, bananas, gold coins, and betel leaves brings prosperity."
        },
        {
            "id": "pu5",
            "question": "What traditional greeting do people exchange on Tamil New Year?",
            "options": ["Iniya Tamizh Puthandu Nalvazhthukkal!", "Pongalo Pongal!", "Deepavali Vazhthukkal!", "Vanakkam Thambi!"],
            "answer_index": 0,
            "explanation": "'Iniya Tamizh Puthandu Nalvazhthukkal' means wishing you a sweet and prosperous Tamil New Year."
        },
        {
            "id": "pu6",
            "question": "What astronomical almanac reading takes place in temples on New Year day?",
            "options": ["Panchangam Sravanam (Reading solar and planetary movements)", "Weather Forecast", "Book Fair", "Horoscope Contest"],
            "answer_index": 0,
            "explanation": "Elders listen to the reading of the new Panchangam almanac for agricultural and spiritual guidance."
        },
        {
            "id": "pu7",
            "question": "Which trio of sacred fruits ('Mukkani') are offered on Puthandu?",
            "options": ["Ma, Pala, Vaazhai (Mango, Jackfruit, Banana)", "Apple, Orange, Grape", "Guava, Papaya, Fig", "Watermelon, Kiwi, Peach"],
            "answer_index": 0,
            "explanation": "The three royal fruits of Tamil Nadu are Mango (Maa), Jackfruit (Palaa), and Banana (Vaazhai)."
        },
        {
            "id": "pu8",
            "question": "What type of traditional garments do family members wear on Puthandu morning?",
            "options": ["New traditional silk clothes (Pattu Pavadai / Veshti)", "Raincoats", "Casual sports jerseys", "Old winter coats"],
            "answer_index": 0,
            "explanation": "Wearing fresh, pristine traditional clothes signifies turning a new, bright chapter in life."
        },
        {
            "id": "pu9",
            "question": "What colorful powder designs are drawn in front of homes on New Year morning?",
            "options": ["Intricate Floral Kolam with colored powders", "Spray painting", "Oil pastel canvas", "Chalk numbers"],
            "answer_index": 0,
            "explanation": "Vibrant festive Kolams with rice flour and flower petals decorate every doorstep."
        },
        {
            "id": "pu10",
            "question": "What value does Puthandu teach children for the upcoming year?",
            "options": ["Optimism, respect for elders, and embracing all experiences with joy", "Winning arguments", "Spending allowance quickly", "Staying up late"],
            "answer_index": 0,
            "explanation": "Puthandu instills optimism, gratitude, and setting noble goals for learning and character."
        }
    ],
    "karthigai_deepam": [
        {
            "id": "kd1",
            "question": "What sacred object is lit in hundreds across homes during Karthigai Deepam?",
            "options": ["Agal Vilakku (Terracotta Clay Oil Lamps)", "Candles only", "Paper lanterns", "Electric LED strip"],
            "answer_index": 0,
            "explanation": "Clay Agal Vilakku filled with fragrant sesame oil and cotton wicks are lit in rows."
        },
        {
            "id": "kd2",
            "question": "On which famous holy mountain in Tamil Nadu is the colossal Maha Deepam lit atop the peak?",
            "options": ["Thiruvannamalai (Annamalai Hill)", "Palani Hill", "Western Ghats", "Nilgiri Peak"],
            "answer_index": 0,
            "explanation": "At Thiruvannamalai, a massive copper cauldron of ghee is lit into a giant beacon visible for miles."
        },
        {
            "id": "kd3",
            "question": "What spiritual truth does the flame of the Deepam symbolize?",
            "options": ["Knowledge dispelling the darkness of ignorance and ego", "Physical warmth only", "Cooking fire", "Night light"],
            "answer_index": 0,
            "explanation": "The flame symbolizes the divine spark of wisdom (Jnana) that destroys ignorance and fear."
        },
        {
            "id": "kd4",
            "question": "What type of traditional oil is considered most auspicious for lighting clay deepams?",
            "options": ["Pure Gingelly (Sesame) Oil or Cow's Ghee", "Refined sunflower oil", "Mineral oil", "Motor oil"],
            "answer_index": 0,
            "explanation": "Sesame oil (Nallennai) and pure ghee are traditionally believed to bring positive spiritual vibrations."
        },
        {
            "id": "kd5",
            "question": "What sweet roasted paddy treat is lovingly prepared for Karthigai Deepam?",
            "options": ["Nel Pori Urundai (Crisp puffed rice balls with jaggery)", "Gulab Jamun", "Chocolate cake", "Carrot Halwa"],
            "answer_index": 0,
            "explanation": "Pori Urundai made from crisp puffed paddy and melted jaggery syrup is the classic Karthigai offering."
        },
        {
            "id": "kd6",
            "question": "On which lunar phase does Karthigai Deepam always occur?",
            "options": ["Pournami (Full Moon Night)", "Amavasya (New Moon Night)", "Ashtami", "Ekadashi"],
            "answer_index": 0,
            "explanation": "It falls on the full moon night in the month of Karthigai aligned with the Krittika star."
        },
        {
            "id": "kd7",
            "question": "What constellation of six stars in astronomy is associated with Karthigai?",
            "options": ["Pleiades (Six Krittika maidens)", "Orion's Belt", "Great Bear", "Cassiopeia"],
            "answer_index": 0,
            "explanation": "The Krittika star cluster is associated with the 6 Krittika foster mothers of Lord Murugan."
        },
        {
            "id": "kd8",
            "question": "Where are deepams placed around the traditional Indian home?",
            "options": ["Along doorways, windows, balconies, and kolams", "Inside dark closets only", "Under the bed", "In the refrigerator"],
            "answer_index": 0,
            "explanation": "Lamps are placed all along the threshold, stairs, and verandas to illuminate every corner."
        },
        {
            "id": "kd9",
            "question": "What direction is considered auspicious when lighting the tip of the wick?",
            "options": ["Facing East or North", "Facing South only", "Facing directly downward", "Any random corner"],
            "answer_index": 0,
            "explanation": "Pointing the wick East or North welcomes health, peace, and spiritual illumination."
        },
        {
            "id": "kd10",
            "question": "What ancient Tamil Sangam literature mentions the timeless festival of lights?",
            "options": ["Akananuru and Kalavazhi Narpadhu", "Modern newspaper", "English dictionary", "Science textbook"],
            "answer_index": 0,
            "explanation": "Karthigai Deepam is one of the oldest recorded Tamil festivals, celebrated for over 2,500 years."
        }
    ],
    "thaipusam": [
        {
            "id": "tp1",
            "question": "Who is the primary deity honored with immense devotion on Thaipusam?",
            "options": ["Lord Murugan (Kartikeya / Skanda)", "Lord Indra", "Lord Brahma", "Lord Varuna"],
            "answer_index": 0,
            "explanation": "Thaipusam celebrates Lord Murugan receiving the sacred Vel (spear of wisdom) from Goddess Parvati."
        },
        {
            "id": "tp2",
            "question": "What color clothes do devotees traditionally wear during Thaipusam pilgrimages?",
            "options": ["Bright Yellow or Saffron", "Black only", "Dark Blue", "Grey"],
            "answer_index": 0,
            "explanation": "Yellow and saffron symbolize purity, spiritual wisdom, and devotion to Lord Murugan."
        },
        {
            "id": "tp3",
            "question": "What wooden or metal arched structure decorated with peacock feathers do devotees carry on their shoulders?",
            "options": ["Kavadi", "Chariot", "Palanquin", "Umbrella"],
            "answer_index": 0,
            "explanation": "The Kavadi is an ornate arch carried on the shoulders as a vow of devotion and self-discipline."
        },
        {
            "id": "tp4",
            "question": "What famous landmark cave temple in Malaysia is world-renowned for its giant golden Murugan statue and Thaipusam procession?",
            "options": ["Batu Caves (Kuala Lumpur)", "Ajanta Caves", "Elephanta Caves", "Ellora Caves"],
            "answer_index": 0,
            "explanation": "Batu Caves in Malaysia has a majestic 140-foot golden Murugan statue and 272 colorful temple steps."
        },
        {
            "id": "tp5",
            "question": "What does Lord Murugan's sacred spear (the 'Vel') represent philosophically?",
            "options": ["Sharp, broad, and deep spiritual intellect and wisdom", "Physical weapon only", "A ruler's crown", "A decorative flag"],
            "answer_index": 0,
            "explanation": "The Vel represents wisdom that is sharp at the point, broad at the middle, and deep at the shaft."
        },
        {
            "id": "tp6",
            "question": "What cooling dairy offering carried in small brass pots is poured over the deity during Thaipusam?",
            "options": ["Paal Kudam (Milk Pots)", "Cold water only", "Coconut oil only", "Honey bowl only"],
            "answer_index": 0,
            "explanation": "Devotees carry Paal Kudam (pots of pure milk) on their heads as an offering of peace and gratitude."
        },
        {
            "id": "tp7",
            "question": "What majestic bird is Lord Murugan's divine vehicle (Vahana)?",
            "options": ["The Peacock (Mayil)", "The Swan", "The Eagle", "The Bull"],
            "answer_index": 0,
            "explanation": "The peacock represents the destruction of arrogance and pride beneath divine wisdom."
        },
        {
            "id": "tp8",
            "question": "What chant do devotees joyfully proclaim along the pilgrimage path?",
            "options": ["Vetrivel Muruganukku... Haroharohara!", "Om Namah Shivaya", "Hare Krishna", "Jai Ganesha"],
            "answer_index": 0,
            "explanation": "'Vetrivel Muruganukku Haroharohara' celebrates the victorious spear of Lord Murugan."
        },
        {
            "id": "tp9",
            "question": "In which Tamil month does Thaipusam take place?",
            "options": ["Thai (January - February)", "Chithirai", "Aavani", "Purattasi"],
            "answer_index": 0,
            "explanation": "Thaipusam occurs on the full moon day of the month of Thai when the Pusam star shines brightest."
        },
        {
            "id": "tp10",
            "question": "What character quality does Thaipusam encourage children to cultivate?",
            "options": ["Courage, endurance, focus, and overcoming fear", "Being lazy", "Giving up easily", "Seeking attention"],
            "answer_index": 0,
            "explanation": "Thaipusam inspires mental strength, focus, courage, and perseverance in the face of all difficulties."
        }
    ],
    "vinayagar_chaturthi": [
        {
            "id": "vct1",
            "question": "What sweet steamed delicacy filled with grated coconut and jaggery is Lord Vinayagar's most beloved offering?",
            "options": ["Kozhukattai / Modak (கொழுக்கட்டை)", "Gulab Jamun", "Mysore Pak", "Jalebi"],
            "answer_index": 0,
            "explanation": "Sweet Kozhukattai made with steamed rice flour dough, jaggery, and coconut poornam is the crown sweet of Vinayagar Chaturthi."
        },
        {
            "id": "vct2",
            "question": "What humble, observant creature is Lord Vinayagar's faithful vehicle (Vahana)?",
            "options": ["Mooshika the Mouse (மூஷிக வாகனம்)", "Mayil (The Peacock)", "Nandi (The Bull)", "Garuda (The Eagle)"],
            "answer_index": 0,
            "explanation": "Mooshika the tiny mouse teaches us humility, mindfulness, and that even the smallest being has great divine purpose."
        },
        {
            "id": "vct3",
            "question": "What fresh green grass blades are specially gathered and offered in garlands to Lord Pillaiyar?",
            "options": ["Arugampul (அறுகம்புல் / Bermuda Grass)", "Tulsi leaves only", "Neem leaves", "Banana leaves"],
            "answer_index": 0,
            "explanation": "Arugampul has ancient medicinal and cooling properties, making it the most sacred offering for Pillaiyar."
        },
        {
            "id": "vct4",
            "question": "What famous Tamil devotional children's song begins with 'Pillaiyare Pillaiyare...'?",
            "options": ["'Pillaiyare Pillaiyare Perumai Vaintha Pillaiyare' (பிள்ளையாரே பிள்ளையாரே)", "Kanda Sashti Kavasam", "Thiruppavai", "Thevaram"],
            "answer_index": 0,
            "explanation": "Generations of Tamil children learn to sing 'Pillaiyare Pillaiyare Perumai Vaintha Pillaiyare' celebrating his loving protection."
        },
        {
            "id": "vct5",
            "question": "What eco-friendly natural material is traditionally used to mould Pillaiyar idols at home?",
            "options": ["Natural river clay (களிமண் பிள்ளையார் / Man Pillaiyar)", "Plastic", "Plaster of Paris with synthetic paints", "Cement"],
            "answer_index": 0,
            "explanation": "Moulding clay Pillaiyars dissolves naturally back into rivers and oceans during Visarjan, protecting nature."
        },
        {
            "id": "vct6",
            "question": "Why is Lord Vinayagar worshipped first before starting any new school year, exam, or auspicious journey?",
            "options": ["He is the Vighnaharta / Muzhumudhar Kadavul (முழுமுதற் கடவுள் - Remover of all hurdles)", "He loves celebrations", "He is the oldest deity", "He carries sweets"],
            "answer_index": 0,
            "explanation": "Vinayagar is revered as the Lord of Auspicious Beginnings who removes obstacles from our studies and paths."
        },
        {
            "id": "vct7",
            "question": "In the famous fruit of wisdom (Gnana Pazham) legend, how did Vinayagar win the divine mango from Sage Narada?",
            "options": ["He circumambulated his parents Lord Shiva and Goddess Parvati, recognizing parents as his entire universe", "He ran faster than Murugan", "He flew on a bird", "He bought another fruit"],
            "answer_index": 0,
            "explanation": "Vinayagar wisely showed that parents are one's living universe, earning the Gnana Pazham mango of wisdom."
        },
        {
            "id": "vct8",
            "question": "Which great saint-poetess of Tamil Nadu composed the revered 'Vinayagar Agaval'?",
            "options": ["Avvaiyar (ஔவையார்)", "Karaikkal Ammaiyar", "Andal", "Mangayarkkarasiyar"],
            "answer_index": 0,
            "explanation": "The wise sage Avvaiyar composed the timeless 'Vinayagar Agaval' praising Lord Ganesha's spiritual wisdom."
        },
        {
            "id": "vct9",
            "question": "What traditional posture of holding the earlobes and doing squats is practiced before Lord Vinayagar?",
            "options": ["Thoppukaranam (தோப்புக் கரணம் / Super Brain Yoga)", "Clapping hands", "Snapping fingers", "Standing on one leg"],
            "answer_index": 0,
            "explanation": "Thoppukaranam stimulates acupuncture points in the earlobes, scientifically activating both hemispheres of the brain."
        },
        {
            "id": "vct10",
            "question": "What do Lord Ganesha's broad elephant ears remind all young students to practice?",
            "options": ["Listen attentively, absorb good knowledge, and speak thoughtfully", "Talk constantly in class", "Ignore elders", "Listen to loud music"],
            "answer_index": 0,
            "explanation": "Ganesha's large ears symbolize being a great, patient listener and absorbing wisdom with clarity."
        }
    ],
    "ayudha_pooja": [
        {
            "id": "ap1",
            "question": "Which divine Goddess of wisdom, knowledge, arts, and music is revered on Saraswathi Pooja?",
            "options": ["Goddess Saraswathi (சரஸ்வதி தேவி)", "Goddess Lakshmi only", "Goddess Kali only", "Goddess Parvati only"],
            "answer_index": 0,
            "explanation": "Goddess Saraswathi represents divine knowledge, learning, intellect, music, and the arts."
        },
        {
            "id": "ap2",
            "question": "What classical Indian musical instrument does Goddess Saraswathi hold gracefully in her hands?",
            "options": ["The Veena (வீணை)", "Flute", "Mridangam", "Sitar"],
            "answer_index": 0,
            "explanation": "The sacred Veena represents the rhythm of speech, mind control, and harmonious living."
        },
        {
            "id": "ap3",
            "question": "What do students and school children place before Goddess Saraswathi on the evening of the puja?",
            "options": ["School notebooks, textbooks, and pens for divine blessing (புத்தக பூஜை)", "Toys only", "Old clothes", "Video games"],
            "answer_index": 0,
            "explanation": "Placing study books before the Goddess honors learning as a sacred pursuit and seeks blessings for the school year."
        },
        {
            "id": "ap4",
            "question": "What does the noble observance of 'Ayudha Pooja' (ஆயுத பூஜை) celebrate across Tamil Nadu?",
            "options": ["Dignity of labor—blessing the tools, computers, vehicles, and instruments that help us work", "Fighting battles", "Cleaning windows only", "Playing sports only"],
            "answer_index": 0,
            "explanation": "Ayudha Pooja honors every profession by cleaning and blessing the tools, machines, and computers that sustain our livelihood."
        },
        {
            "id": "ap5",
            "question": "What festive sweet snack mixture is joyfully distributed as Prasad on Ayudha Pooja day?",
            "options": ["Pori, Pottukadalai, Jaggery & Coconut (பொரி, பொட்டுக் கடலை, வெல்லம்)", "Potato chips", "Bread slice", "Ice cream"],
            "answer_index": 0,
            "explanation": "Crisp puffed rice (Pori) blended with roasted gram (Pottukadalai), jaggery, peanuts, and coconut is the signature prasad."
        },
        {
            "id": "ap6",
            "question": "What auspicious marks of sandal paste and red vermilion decorate vehicles, bicycles, and toolkits?",
            "options": ["Chandanam and Kumkumam Pottu (சந்தனம் & குங்குமம்)", "Spray paint", "Chalk marks", "Paper stickers only"],
            "answer_index": 0,
            "explanation": "Cooling sandalwood paste and red kumkumam are applied to vehicles and equipment along with fresh flower garlands."
        },
        {
            "id": "ap7",
            "question": "What auspicious ceremony on the following morning (Vijayadashami) marks young children writing their very first letters?",
            "options": ["Vidyarambham / Aksharabhyasam (அட்சராப்பியாசம் - ஏடு தொடங்குதல்)", "Sports tournament", "Exam session", "Fasting day"],
            "answer_index": 0,
            "explanation": "During Vidyarambham, children write 'Om' or their native alphabets in a golden plate of rice to begin education."
        },
        {
            "id": "ap8",
            "question": "In the epic Mahabharata, where did the Pandava princes retrieve their tools and weapons on Vijayadashami?",
            "options": ["From the Shami / Vanni tree (வன்னி மரம்)", "From a cave", "From a mountain peak", "From the ocean"],
            "answer_index": 0,
            "explanation": "The Pandavas retrieved and blessed their weapons from the holy Vanni tree on Vijayadashami before reclaiming justice."
        },
        {
            "id": "ap9",
            "question": "What color garments representing absolute purity and truth does Goddess Saraswathi wear?",
            "options": ["Pristine White Saree (வெள்ளை தாமரை & வெண் பட்டு)", "Black only", "Dark Blue", "Neon Orange"],
            "answer_index": 0,
            "explanation": "White symbolizes spotless purity, truth, and illumination unclouded by ego or delusion."
        },
        {
            "id": "ap10",
            "question": "What timeless life lesson does Ayudha Pooja instill in every student and worker?",
            "options": ["Dignity of labor, respecting our books and craft tools, and treating all work as worship", "Disrespecting study materials", "Avoiding practice", "Wasting learning time"],
            "answer_index": 0,
            "explanation": "Ayudha Pooja teaches that 'Work is Worship' (தொழிலே தெய்வம்) and instills deep respect for knowledge and crafts."
        }
    ],

    # ------------------ TELUGU FESTIVALS ------------------
    "ugadi": [
        {
            "id": "ug1",
            "question": "What is the signature dish prepared on Ugadi combining 6 different flavors?",
            "options": ["Ugadi Pachadi", "Mysore Pak", "Pulihora", "Bobbatlu"],
            "answer_index": 0,
            "explanation": "Ugadi Pachadi combines neem, jaggery, raw mango, tamarind, chili, and salt."
        },
        {
            "id": "ug2",
            "question": "How many tastes (Shadruchulu) are represented in the traditional Ugadi Pachadi?",
            "options": ["6 Tastes", "2 Tastes", "4 Tastes", "8 Tastes"],
            "answer_index": 0,
            "explanation": "The six tastes (Shadruchulu) represent sweet, sour, bitter, tangy, spicy, and salty life experiences."
        },
        {
            "id": "ug3",
            "question": "What do the fresh green mango leaves (Toranalu) tied at the main entrance symbolize?",
            "options": ["Welcoming positive energy, prosperity, and good fortune", "Repelling dust only", "Decoration only", "Sign of rain"],
            "answer_index": 0,
            "explanation": "Mango leaf garlands (Toranalu) purify the home atmosphere and invite auspicious beginnings."
        },
        {
            "id": "ug4",
            "question": "What traditional sweet flatbread filled with sweet lentil paste is enjoyed on Ugadi?",
            "options": ["Bobbatlu (Bhakshalu / Puran Poli)", "Jalebi", "Gulab Jamun", "Kaja"],
            "answer_index": 0,
            "explanation": "Warm Bobbatlu topped with pure ghee is the most beloved festive dessert on Ugadi."
        },
        {
            "id": "ug5",
            "question": "What astrological reading takes place in communities on Ugadi evening?",
            "options": ["Panchanga Sravanam", "Poetry contest", "Music concert", "Drama show"],
            "answer_index": 0,
            "explanation": "Panchanga Sravanam predicts the astrological outlook and auspicious timings for the new year."
        },
        {
            "id": "ug6",
            "question": "What does the word 'Ugadi' mean etymologically in Sanskrit (Yuga + Aadi)?",
            "options": ["The beginning of a new era or astronomical cycle", "The harvest feast", "The flower day", "The sunny morning"],
            "answer_index": 0,
            "explanation": "Derived from 'Yuga' (era) and 'Aadi' (beginning), Ugadi marks the dawn of a fresh cycle."
        },
        {
            "id": "ug7",
            "question": "In which month of the Hindu lunar calendar is Ugadi celebrated?",
            "options": ["Chaitra (First month / Spring)", "Kartika", "Ashada", "Magha"],
            "answer_index": 0,
            "explanation": "Ugadi falls on Chaitra Shukla Padyami, the very first day of the Chaitra lunar month."
        },
        {
            "id": "ug8",
            "question": "What colorful floor patterns decorated with chalk and colors adorn Telugu homes on Ugadi?",
            "options": ["Muggulu (Rangoli)", "Sand art", "Oil paintings", "Paper cutouts"],
            "answer_index": 0,
            "explanation": "Beautiful symmetrical Muggulu adorned with colored powders greet guests at the doorway."
        },
        {
            "id": "ug9",
            "question": "Which states celebrate their traditional New Year on this day under the name Ugadi / Gudi Padwa?",
            "options": ["Andhra Pradesh, Telangana, Karnataka, and Maharashtra", "Punjab and Haryana only", "Kerala and Tamil Nadu only", "Assam only"],
            "answer_index": 0,
            "explanation": "Ugadi is celebrated in Andhra Pradesh, Telangana, and Karnataka, and as Gudi Padwa in Maharashtra."
        },
        {
            "id": "ug10",
            "question": "What essential emotional lesson does the Shadruchulu teach growing children?",
            "options": ["Life has sweet moments and tough moments, and we should face all with balance and courage", "Only look for sweets", "Avoid challenges", "Complain when things get sour"],
            "answer_index": 0,
            "explanation": "It teaches equanimity: welcoming all experiences as opportunities to grow and learn."
        }
    ],
    "sankranti": [
        {
            "id": "sk1",
            "question": "How many days is Makara Sankranti celebrated in Telugu tradition?",
            "options": ["3 to 4 Days (Bhogi, Makara Sankranti, Kanuma, Mukkanuma)", "1 Day", "2 Days", "7 Days"],
            "answer_index": 0,
            "explanation": "Telugu Sankranti is celebrated over 3 to 4 festive days with distinct harvest traditions."
        },
        {
            "id": "sk2",
            "question": "What colorful activity fills the skies during Sankranti afternoons?",
            "options": ["Kite Flying (Patang)", "Drone shows", "Paragliding", "Hot air balloons"],
            "answer_index": 0,
            "explanation": "Children and families take to rooftops to fly colorful kites under the bright winter sun."
        },
        {
            "id": "sk3",
            "question": "Who is the wandering minstrel carrying a musical Tambura and rice pot on his head during Sankranti?",
            "options": ["Haridasu", "Kavadi Bearer", "Poet", "Merchant"],
            "answer_index": 0,
            "explanation": "The Haridasu walks from home to home singing praises of Lord Vishnu and blessing families."
        },
        {
            "id": "sk4",
            "question": "What traditional sweet made from freshly harvested rice flour and jaggery is made for Sankranti?",
            "options": ["Ariselu", "Gulab Jamun", "Jalebi", "Rasgulla"],
            "answer_index": 0,
            "explanation": "Ariselu, a golden deep-fried delicacy made with jaggery, rice flour, and sesame seeds, is the pride of Sankranti."
        },
        {
            "id": "sk5",
            "question": "What are the small decorated cow dung balls placed inside Muggulu with flowers called?",
            "options": ["Gobbemmalu", "Toranalu", "Kalasam", "Deepam"],
            "answer_index": 0,
            "explanation": "Gobbemmalu decorated with yellow marigold petals and turmeric are placed in the center of Muggulu."
        },
        {
            "id": "sk6",
            "question": "Which celestial event gives Makara Sankranti its sacred name?",
            "options": ["The Sun entering the Capricorn (Makara) zodiac sign", "Full moon night", "A solar eclipse", "A comet appearance"],
            "answer_index": 0,
            "explanation": "It marks the Sun's transit (Sankramana) into the Makara (Capricorn) zodiac sign."
        },
        {
            "id": "sk7",
            "question": "What day of the festival is dedicated to farmers thanking their cattle (Kanuma)?",
            "options": ["Day 3: Kanuma", "Day 1: Bhogi", "Day 2: Sankranti", "Day 4: Mukkanuma"],
            "answer_index": 0,
            "explanation": "Kanuma is the day when farmers wash, decorate, and honor their cattle for their help in farming."
        },
        {
            "id": "sk8",
            "question": "What fruit, sugarcane, and coin shower is poured over young children's heads on Bhogi evening?",
            "options": ["Bhogi Pallu (Ber fruits, sugarcane pieces, and coins)", "Flower petals only", "Water splash", "Confetti only"],
            "answer_index": 0,
            "explanation": "Pouring sweet Bhogi Pallu over children's heads is believed to protect them from the evil eye and bless them with long life."
        },
        {
            "id": "sk9",
            "question": "What decorated bull parade accompanied by Shehnai music visits homes on Sankranti?",
            "options": ["Gangireddu", "Jallikattu", "Kambala", "Gajam"],
            "answer_index": 0,
            "explanation": "The Gangireddu bull is elaborately decorated and performs graceful steps to the music of pipers."
        },
        {
            "id": "sk10",
            "question": "What timeless values are celebrated across Makara Sankranti?",
            "options": ["Gratitude to nature, honoring farmers, and sharing harvest bounty with everyone", "Watching television alone", "Spending money on gadgets", "Sleeping through the day"],
            "answer_index": 0,
            "explanation": "Sankranti fosters gratitude to the sun, earth, cattle, and hardworking farmers who sustain society."
        }
    ],
    "bonalu": [
        {
            "id": "bn1",
            "question": "In which Indian state is the grand folk festival of Bonalu celebrated with immense fervor?",
            "options": ["Telangana (Hyderabad and Secunderabad)", "Kerala", "Tamil Nadu", "Gujarat"],
            "answer_index": 0,
            "explanation": "Bonalu is a vibrant state festival of Telangana honoring the Mother Goddess Mahakali."
        },
        {
            "id": "bn2",
            "question": "What does the word 'Bonam' (Bonalu) derive from in Telugu?",
            "options": ["Bhojanam (A meal / Feast offering to the Goddess)", "Deepam", "Flower garland", "Dance"],
            "answer_index": 0,
            "explanation": "'Bonam' comes from 'Bhojanam', representing the loving meal prepared and offered to Goddess Mahakali."
        },
        {
            "id": "bn3",
            "question": "What do women carry balanced gracefully on their heads during the Bonalu procession?",
            "options": ["Decorated earthen pots adorned with neem leaves and turmeric, lit with a diya", "Brass buckets", "Fruit baskets only", "Wooden boxes"],
            "answer_index": 0,
            "explanation": "Women carry decorated pots containing cooked rice, milk, jaggery, neem leaves, and a glowing oil lamp."
        },
        {
            "id": "bn4",
            "question": "Who is the fierce dancing guardian figure with bells, vermilion, and a whip in the Bonalu procession?",
            "options": ["Pothuraju (Brother of the Goddess)", "Haridasu", "Yakshagana dancer", "Kathakali dancer"],
            "answer_index": 0,
            "explanation": "Pothuraju dances energetically with ankle bells and a whip, leading and protecting the procession."
        },
        {
            "id": "bn5",
            "question": "In which month of the Telugu calendar is Bonalu celebrated during the monsoon?",
            "options": ["Ashada Masam (July - August)", "Kartika Masam", "Chaitra Masam", "Magha Masam"],
            "answer_index": 0,
            "explanation": "Bonalu is celebrated throughout the monsoon month of Ashada to seek health and protection from seasonal ailments."
        },
        {
            "id": "bn6",
            "question": "Which historic fort temple in Hyderabad witnesses the very first Bonalu offering of the season?",
            "options": ["Golconda Fort (Jagadamba Temple)", "Warangal Fort", "Charminar", "Ramappa Temple"],
            "answer_index": 0,
            "explanation": "The festival begins at the ancient Sri Jagadambika temple inside the historic Golconda Fort."
        },
        {
            "id": "bn7",
            "question": "What is the prophetic oracle ceremony performed on the day after Bonalu called?",
            "options": ["Rangam (Oracle predictions standing atop an earthen pot)", "Pooja", "Arati", "Bhajan"],
            "answer_index": 0,
            "explanation": "During Rangam, an oracle woman stands on an earthen pot and answers community questions about the upcoming year."
        },
        {
            "id": "bn8",
            "question": "What special tree leaves known for their medicinal and antibacterial properties adorn every Bonam pot?",
            "options": ["Neem leaves (Vepa aaku)", "Banana leaves", "Mango leaves", "Rose petals"],
            "answer_index": 0,
            "explanation": "Neem leaves have powerful natural antibacterial properties used to ward off seasonal illnesses."
        },
        {
            "id": "bn9",
            "question": "What colorful elephant procession carrying the portrait of the Goddess marks the finale of Bonalu?",
            "options": ["Ghatam Procession on a decorated elephant", "Chariot race", "Boat parade", "Horse run"],
            "answer_index": 0,
            "explanation": "The royal Ghatam procession atop an elephant marches through the streets of Old City Hyderabad."
        },
        {
            "id": "bn10",
            "question": "What community spirit does Bonalu celebrate among families and neighborhoods?",
            "options": ["Community solidarity, health protection, cultural folk arts, and women's leadership", "Watching movies alone", "Staying indoors", "Competitive gaming"],
            "answer_index": 0,
            "explanation": "Bonalu celebrates neighborhood unity, rich folk rhythms (Dappu drums), and honoring the protective divine feminine."
        }
    ],

    # ------------------ MALAYALAM FESTIVALS ------------------
    "onam": [
        {
            "id": "on1",
            "question": "Which beloved legendary King's annual homecoming is celebrated during Onam in Kerala?",
            "options": ["King Mahabali (Maveli)", "King Vikramaditya", "King Ashoka", "King Harsha"],
            "answer_index": 0,
            "explanation": "Onam welcomes the benevolent Asura king Mahabali, who returns every year to visit his prosperous subjects."
        },
        {
            "id": "on2",
            "question": "What circular flower carpet created on the floor with fresh petals is made during Onam?",
            "options": ["Athapookalam", "Kolam", "Muggulu", "Alpana"],
            "answer_index": 0,
            "explanation": "Athapookalam is an intricate, multi-layered circular floral carpet designed from Atham to Thiruvonam."
        },
        {
            "id": "on3",
            "question": "What grand traditional vegetarian feast served on a plantain leaf is the highlight of Onam?",
            "options": ["Onasadya (featuring up to 26 dishes)", "Biryani", "Pongal plate", "Pulao"],
            "answer_index": 0,
            "explanation": "The Onasadya is a spectacular 26-dish traditional feast served on a fresh banana leaf."
        },
        {
            "id": "on4",
            "question": "What exciting boat races featuring long traditional snake boats take place on Kerala backwaters?",
            "options": ["Vallamkali (Snake Boat Race / Nehru Trophy)", "Kayak sprint", "Motorboat race", "Rafting"],
            "answer_index": 0,
            "explanation": "Vallamkali features hundreds of rowers singing rhythmic Vanchipattu songs propelling long snake boats (Chundan Vallam)."
        },
        {
            "id": "on5",
            "question": "What is the famous energetic tiger dance performed by artists painted like tigers during Onam?",
            "options": ["Pulikali (Tiger Dance)", "Kathakali", "Mohiniyattam", "Theyyam"],
            "answer_index": 0,
            "explanation": "In Pulikali, performers paint their bodies with bright yellow, black, and red stripes to dance like tigers to traditional beats."
        },
        {
            "id": "on6",
            "question": "How many days is the Onam festival celebrated from Atham to Thiruvonam?",
            "options": ["10 Days", "3 Days", "5 Days", "14 Days"],
            "answer_index": 0,
            "explanation": "Onam festivities span 10 joyous days starting from the asterism of Atham and culminating on Thiruvonam."
        },
        {
            "id": "on7",
            "question": "Which avatar of Lord Vishnu visited King Mahabali before granting him the boon to visit his people annually?",
            "options": ["Vamana (The dwarf Brahmin avatar)", "Narasimha", "Rama", "Varaha"],
            "answer_index": 0,
            "explanation": "Lord Vishnu appeared as Vamana, testing King Mahabali's humility and truthfulness."
        },
        {
            "id": "on8",
            "question": "What sweet dessert made from jaggery, coconut milk, and rice/lentils is served at the end of the Onasadya?",
            "options": ["Payasam (Ada Pradhaman / Palada)", "Gulab Jamun", "Kulfi", "Rasgulla"],
            "answer_index": 0,
            "explanation": "Warm, creamy Payasam made with coconut milk and jaggery is the crown jewel of the Onam feast."
        },
        {
            "id": "on9",
            "question": "What traditional cream-and-gold handloom attire do women wear during Onam celebrations?",
            "options": ["Kasavu Saree / Set Mundu", "Kanjeevaram Silk", "Bandhani Saree", "Banarasi Saree"],
            "answer_index": 0,
            "explanation": "The elegant off-white Kasavu saree with golden Zari borders is the timeless dress of Kerala."
        },
        {
            "id": "on10",
            "question": "What famous ancient proverb summarizes the equality and joy during King Mahabali's reign?",
            "options": ["'Maveli naadu vaanidum kaalam, maanusharellarum onnupole' (All humans lived as equals in harmony)", "'Survival of the fittest'", "'Might is right'", "'Time is money'"],
            "answer_index": 0,
            "explanation": "The song celebrates an ideal society where all people were treated equally, with no deceit, theft, or sorrow."
        }
    ],

    # ------------------ HINDI CULTURAL FESTIVALS ------------------
    "holi": [
        {
            "id": "hl1",
            "question": "What is Holi joyfully celebrated as across North India and the world?",
            "options": ["The Festival of Colors (रंगों का त्योहार)", "The Festival of Lights", "The Festival of Kites", "The Festival of Flowers"],
            "answer_index": 0,
            "explanation": "Holi is the world-famous Festival of Colors marking the arrival of spring, joy, and new beginnings."
        },
        {
            "id": "hl2",
            "question": "Which young, devoted prince was saved from fire by Lord Vishnu during the Holika Dahan bonfire?",
            "options": ["Bhakt Prahlad (भक्त प्रह्लाद)", "Prince Dhruva", "Prince Bharata", "Prince Angad"],
            "answer_index": 0,
            "explanation": "Bhakt Prahlad's supreme faith in Lord Vishnu protected him, while the demoness Holika perished in the fire."
        },
        {
            "id": "hl3",
            "question": "What traditional crescent-shaped sweet dumpling filled with khoya and nuts is prepared for Holi?",
            "options": ["Gujiya (गुझिया)", "Modak", "Jalebi", "Rasgulla"],
            "answer_index": 0,
            "explanation": "Crispy golden Gujiya filled with sweet mawa (khoya), coconut, and cardamom is the quintessential Holi sweet."
        },
        {
            "id": "hl4",
            "question": "What natural, vibrant dry colored powder is smeared on cheeks to celebrate Holi friendship?",
            "options": ["Gulal (गुलाल) and Abeer", "Chalk powder", "Sand", "Charcoal"],
            "answer_index": 0,
            "explanation": "Organic Gulal made from flower petals like Palash (Flame of the Forest) is used to share colorful love."
        },
        {
            "id": "hl5",
            "question": "What season (Ritu) does Holi joyfully welcome in the Indian calendar?",
            "options": ["Vasant Ritu (Spring Season)", "Varsha Ritu (Monsoon)", "Shishir (Winter)", "Grishma (Summer)"],
            "answer_index": 0,
            "explanation": "Holi celebrates Vasant Ritu (spring) when flowers bloom, crops ripen, and winter cold fades away."
        },
        {
            "id": "hl6",
            "question": "On the night before playing with colors, what ritual bonfire is lit to destroy negativity?",
            "options": ["Holika Dahan (होलिका दहन)", "Lohri Bonfire", "Deepam", "Hawan only"],
            "answer_index": 0,
            "explanation": "Holika Dahan bonfires are lit on the full moon night (Phalguna Purnima) symbolizing the victory of devotion over evil."
        },
        {
            "id": "hl7",
            "question": "In which historic town in Braj (Uttar Pradesh) is the famous 'Lathmar Holi' playfully celebrated?",
            "options": ["Barsana and Nandgaon", "Jaipur", "Varanasi", "Patna"],
            "answer_index": 0,
            "explanation": "In Barsana, women playfully reenact Krishna's visits by tapping shields with decorative sticks."
        },
        {
            "id": "hl8",
            "question": "What cooling traditional beverage flavored with saffron, almonds, and rose petals is served on Holi?",
            "options": ["Thandai (ठंडाई)", "Filter Coffee", "Mango Shake", "Lassi only"],
            "answer_index": 0,
            "explanation": "Chilled Thandai infused with fennel, cardamom, almonds, and saffron is the classic Holi festive drink."
        },
        {
            "id": "hl9",
            "question": "What famous traditional phrase is shouted when playfully coloring friends and family?",
            "options": ["'Bura na mano, Holi hai!' (बुरा न मानो, होली है!)", "'Jai Ho!'", "'Shubh Deepavali!'", "'Vanakkam!'"],
            "answer_index": 0,
            "explanation": "'Bura na mano, Holi hai!' means 'Do not take offense, let us celebrate and share joy!'."
        },
        {
            "id": "hl10",
            "question": "What vital moral lesson does Holi teach all children?",
            "options": ["Forgiving past misunderstandings, spreading happiness, and embracing equality", "Winning every argument", "Staying quiet", "Eating alone"],
            "answer_index": 0,
            "explanation": "Holi breaks down all barriers of age and background, encouraging forgiveness, warm embraces, and joyful unity."
        }
    ],
    "dussehra": [
        {
            "id": "ds1",
            "question": "What epic victory does Dussehra (Vijayadashami) celebrate in the Ramayana?",
            "options": ["Lord Rama's victory over the demon king Ravana", "Lord Krishna lifting Govardhan", "Pandavas winning Kurukshetra", "Lord Shiva's cosmic dance"],
            "answer_index": 0,
            "explanation": "Dussehra celebrates Lord Rama defeating the ten-headed demon king Ravana, rescuing Sita, and establishing Dharma."
        },
        {
            "id": "ds2",
            "question": "How many heads did the powerful demon king of Lanka, Ravana, possess?",
            "options": ["10 Heads (दशानन)", "5 Heads", "8 Heads", "12 Heads"],
            "answer_index": 0,
            "explanation": "Ravana was known as Dashanana (ten-headed), representing immense knowledge combined with destructive ego."
        },
        {
            "id": "ds3",
            "question": "What dramatic stage performances depicting Lord Rama's life are enacted across North India leading up to Dussehra?",
            "options": ["Ramlila (रामलीला)", "Kathakali", "Bhangra", "Nautanki"],
            "answer_index": 0,
            "explanation": "Ramlila plays are staged in neighborhood grounds for ten nights, culminating in the burning of Ravana's effigy."
        },
        {
            "id": "ds4",
            "question": "Whose giant firecracker-filled effigies are burned on Dussehra evening?",
            "options": ["Ravana, Kumbhakarna, and Meghnada (Indrajit)", "Forest bandits", "Old toys", "Straw monsters"],
            "answer_index": 0,
            "explanation": "Giant towering effigies of Ravana and his brothers are set ablaze to symbolize the end of arrogance and evil."
        },
        {
            "id": "ds5",
            "question": "Which divine Goddess also conquered the demon Mahishasura on the tenth day of Vijayadashami?",
            "options": ["Goddess Durga (Maa Durga)", "Goddess Saraswati", "Goddess Lakshmi", "Goddess Ganga"],
            "answer_index": 0,
            "explanation": "Goddess Durga slayed the buffalo-demon Mahishasura on Vijayadashami after a nine-day battle."
        },
        {
            "id": "ds6",
            "question": "In the royal city of Mysuru (Karnataka), how is Dussehra celebrated with world-famous grandeur?",
            "options": ["Illuminating the Royal Palace with 100,000 lights and the Jumboo Savari elephant procession", "Kite flying contest", "Beach sports", "Boat racing"],
            "answer_index": 0,
            "explanation": "Mysuru Dasara features a grand golden chariot procession carried by decorated royal elephants."
        },
        {
            "id": "ds7",
            "question": "What tree's sacred leaves (representing gold) are exchanged as tokens of goodwill in Maharashtra and MP on Dussehra?",
            "options": ["Apta / Shami tree leaves ('Sona')", "Neem leaves", "Peepal leaves", "Banana leaves"],
            "answer_index": 0,
            "explanation": "Apta tree leaves, known as 'Sona' (gold), are exchanged among elders and friends to wish prosperity."
        },
        {
            "id": "ds8",
            "question": "What auspicious learning ceremony for children begins on Vijayadashami day?",
            "options": ["Vidyarambham (Inauguration of education, arts, and letters)", "Sports training", "Exam day", "Fasting"],
            "answer_index": 0,
            "explanation": "Vijayadashami is considered the most auspicious day for young children to write their first letters and start music or dance."
        },
        {
            "id": "ds9",
            "question": "Who was the devoted brother of Ravana who chose truth and Dharma to support Lord Rama?",
            "options": ["Vibhishana", "Kumbhakarna", "Meghnada", "Maricha"],
            "answer_index": 0,
            "explanation": "Vibhishana stood for righteousness and truth, counseling Ravana before joining Lord Rama."
        },
        {
            "id": "ds10",
            "question": "What is the timeless moral message of Dussehra for every child?",
            "options": ["Truth, courage, and goodness (Dharma) will always triumph over arrogance and falsehood", "Might makes right", "Money buys everything", "Anger solves problems"],
            "answer_index": 0,
            "explanation": "Dussehra reminds us to eliminate internal vices (anger, pride, greed) and uphold truth and kindness in all situations."
        }
    ],
    "raksha_bandhan": [
        {
            "id": "rb1",
            "question": "What is the literal meaning of 'Raksha Bandhan' in Sanskrit and Hindi?",
            "options": ["The Sacred Bond of Protection and Love (सुरक्षा और प्रेम का बंधन)", "Festival of Sweets", "Sister's Day", "Brother's Birthday"],
            "answer_index": 0,
            "explanation": "'Raksha' means protection and 'Bandhan' means a bond, celebrating the protective, caring connection between siblings."
        },
        {
            "id": "rb2",
            "question": "What sacred decorative thread do sisters lovingly tie on their brothers' right wrists?",
            "options": ["Rakhi (राखी)", "Kangan", "Gold chain", "Ribbon"],
            "answer_index": 0,
            "explanation": "The Rakhi is a sacred, colorful thread imbued with prayers for the brother's long life and prosperity."
        },
        {
            "id": "rb3",
            "question": "What auspicious mark is placed on the brother's forehead during the Rakhi ritual?",
            "options": ["Roli Tikka (Tilak with unbroken rice / Akshat)", "Mehendi", "Kajal", "Water drop"],
            "answer_index": 0,
            "explanation": "The red Roli Tilak with unbroken rice grains (Akshat) represents victory, intellect, and divine blessing."
        },
        {
            "id": "rb4",
            "question": "What lifelong promise do brothers make to their sisters after receiving the Rakhi?",
            "options": ["To stand by them, protect them, and support them through all life's moments", "To do their chores", "To share toys for one day", "To win a game"],
            "answer_index": 0,
            "explanation": "Brothers present gifts and pledge lifelong love, respect, and mutual protection to their sisters."
        },
        {
            "id": "rb5",
            "question": "On which lunar day of the Hindu calendar is Raksha Bandhan celebrated?",
            "options": ["Shravana Purnima (Full Moon Day in August)", "Kartik Amavasya", "Chaitra Navami", "Magha Purnima"],
            "answer_index": 0,
            "explanation": "Raksha Bandhan is celebrated on the bright full moon day of the holy monsoon month of Shravana."
        },
        {
            "id": "rb6",
            "question": "In the Mahabharata, who tore a piece of her silk sari to bandage Lord Krishna's wounded finger?",
            "options": ["Draupadi (द्रौपदी)", "Kunti", "Gandhari", "Subhadra"],
            "answer_index": 0,
            "explanation": "Draupadi bandaged Krishna's bleeding finger with her sari, and Krishna promised to protect her forever in return."
        },
        {
            "id": "rb7",
            "question": "In medieval Indian history, which Queen of Mewar sent a Rakhi to Mughal Emperor Humayun seeking friendship and help?",
            "options": ["Rani Karnavati of Chittorgarh", "Rani Lakshmibai", "Rani Padmini", "Ahilyabai Holkar"],
            "answer_index": 0,
            "explanation": "Rani Karnavati sent a Rakhi to Humayun, who immediately rode with his army to honor the sacred sibling bond."
        },
        {
            "id": "rb8",
            "question": "What sweet dessert made from condensed milk and nuts is commonly shared after tying the Rakhi?",
            "options": ["Kaju Katli, Ghevar, and Laddoos", "Salted chips", "Bitter herbs", "Pickles only"],
            "answer_index": 0,
            "explanation": "Sisters feed delicious Indian sweets like Kaju Katli, Ghevar, and Motichoor laddoos to their brothers."
        },
        {
            "id": "rb9",
            "question": "Who else do people tie Rakhis to as a mark of deep respect and gratitude across India?",
            "options": ["Indian Soldiers guarding the borders, police officers, and close friends", "Movie actors only", "Foreign tourists only", "Robots"],
            "answer_index": 0,
            "explanation": "Citizens and school children send Rakhis to brave soldiers stationed at distant borders to thank them for protecting the nation."
        },
        {
            "id": "rb10",
            "question": "What core moral value does Raksha Bandhan celebrate in modern society?",
            "options": ["Mutual respect between genders, family unity, and caring for one another", "Buying the most expensive gifts", "Competition", "Jealousy"],
            "answer_index": 0,
            "explanation": "Raksha Bandhan strengthens family bonds, mutual respect, and unconditional love across generations."
        }
    ],
    "janmashtami": [
        {
            "id": "jm1",
            "question": "Whose joyous birth as the eighth avatar of Lord Vishnu is celebrated on Janmashtami?",
            "options": ["Lord Krishna (भगवान श्रीकृष्ण)", "Lord Rama", "Lord Ganesha", "Lord Kartikeya"],
            "answer_index": 0,
            "explanation": "Janmashtami celebrates the divine birth of Lord Krishna in Mathura to defeat evil king Kamsa."
        },
        {
            "id": "jm2",
            "question": "What favorite dairy treat was little Bal Gopal famous for lovingly stealing with his friends?",
            "options": ["Fresh White Butter (Makhan / माखन)", "Ice cream", "Paneer", "Milk chocolate"],
            "answer_index": 0,
            "explanation": "Little Krishna is fondly called 'Makhan Chor' (butter thief) for playfully climbing up to reach pots of fresh butter."
        },
        {
            "id": "jm3",
            "question": "In which city of Uttar Pradesh was baby Krishna born in prison on a stormy midnight?",
            "options": ["Mathura (मथुरा)", "Ayodhya", "Varanasi", "Prayagraj"],
            "answer_index": 0,
            "explanation": "Krishna was born in a prison cell in Mathura to Devaki and Vasudeva before being taken to Gokul."
        },
        {
            "id": "jm4",
            "question": "What thrilling festival sport involves human pyramids climbing high to break an earthen pot of curd?",
            "options": ["Dahi Handi (दही हांडी)", "Kabaddi", "Kho Kho", "Gilli Danda"],
            "answer_index": 0,
            "explanation": "In Maharashtra and North India, spirited teams (Govindas) build multi-tiered human pyramids to break the Dahi Handi."
        },
        {
            "id": "jm5",
            "question": "What musical instrument does Lord Krishna play that enchants all cows, birds, and nature in Vrindavan?",
            "options": ["Bansuri / Flute (बांसुरी)", "Veena", "Tabla", "Sitar"],
            "answer_index": 0,
            "explanation": "Lord Krishna's divine flute (Muralidhar) produces heavenly melodies that calm all living beings."
        },
        {
            "id": "jm6",
            "question": "What beautiful feather does Lord Krishna always wear gracefully in his headpiece?",
            "options": ["Peacock Feather (मोर पंख)", "Swan feather", "Parrot feather", "Eagle feather"],
            "answer_index": 0,
            "explanation": "The peacock feather in Krishna's crown represents beauty, royalty, and nature's vibrant grace."
        },
        {
            "id": "jm7",
            "question": "Who was Krishna's brave father who carried him across the flooded Yamuna river inside a wicker basket?",
            "options": ["Vasudeva (वसुदेव)", "Nanda Baba", "Dasharatha", "Janaka"],
            "answer_index": 0,
            "explanation": "Vasudeva carried baby Krishna across the surging Yamuna river under the multi-headed serpent Sheshnag's hood."
        },
        {
            "id": "jm8",
            "question": "At what time of the night is Lord Krishna's birth celebrated with bells, conch shells, and aarti in temples?",
            "options": ["Midnight (12:00 AM)", "Sunrise (6:00 AM)", "Noon (12:00 PM)", "Sunset (6:00 PM)"],
            "answer_index": 0,
            "explanation": "Because Krishna was born at midnight on Ashtami, temples hold midnight Abhishek and rocking of Bal Gopal in the swing (Jhula)."
        },
        {
            "id": "jm9",
            "question": "What beloved childhood friend of Krishna brought him a simple handful of flattened rice (Poha)?",
            "options": ["Sudama (सुदामा)", "Arjuna", "Balarama", "Uddhava"],
            "answer_index": 0,
            "explanation": "Sudama visited Krishna in Dwarka with a humble gift of Poha, and Krishna treated his childhood friend like a king."
        },
        {
            "id": "jm10",
            "question": "What sacred scripture contains Lord Krishna's timeless wisdom given to Arjuna on the battlefield?",
            "options": ["Shrimad Bhagavad Gita (श्रीमद्भगवद्गीता)", "Ramayana", "Panchatantra", "Hitopadesha"],
            "answer_index": 0,
            "explanation": "The Bhagavad Gita contains Krishna's profound guidance on duty (Karma Yoga), selfless action, and courage."
        }
    ],
    "navratri": [
        {
            "id": "nv1",
            "question": "What does the Sanskrit word 'Navratri' literally translate to?",
            "options": ["Nine Sacred Nights (नौ पवित्र रातें)", "Nine Bright Days", "Nine Sweets", "Nine Temples"],
            "answer_index": 0,
            "explanation": "'Nava' means nine and 'Ratri' means nights, dedicating nine divine nights to worshipping Goddess Durga."
        },
        {
            "id": "nv2",
            "question": "Which supreme Goddess and her 9 divine incarnations (Navadurga) are celebrated during Navratri?",
            "options": ["Goddess Durga (Maa Durga / Shaktirupa)", "Goddess Ganga", "Goddess Yamuna", "Goddess Rati"],
            "answer_index": 0,
            "explanation": "The nine forms (Shailaputri, Brahmacharini, Chandraghanta, Kushmanda, Skandamata, Katyayani, Kalaratri, Mahagauri, Siddhidatri) are worshipped."
        },
        {
            "id": "nv3",
            "question": "What vibrant, energetic folk circle dance performed with decorated sticks is celebrated during Navratri nights?",
            "options": ["Garba and Dandiya Raas (गरबा और डांडिया)", "Bhangra", "Kathak", "Bharatanatyam"],
            "answer_index": 0,
            "explanation": "Garba and Dandiya Raas are traditional folk dances celebrating rhythmic unity around the sacred lamp (Deepa)."
        },
        {
            "id": "nv4",
            "question": "Which tyrannical buffalo-demon was conquered by Goddess Durga to protect the heavens and earth?",
            "options": ["Mahishasura (महिषासुर)", "Ravana", "Kamsa", "Hiranyakashipu"],
            "answer_index": 0,
            "explanation": "Goddess Durga earned the title 'Mahishasuramardini' by defeating the shape-shifting demon Mahishasura."
        },
        {
            "id": "nv5",
            "question": "What special ritual on Ashtami or Navami day honors nine young girls as living embodiments of Maa Durga?",
            "options": ["Kanya Pujan / Kanjak (कन्या पूजन)", "Vidyarambham", "Aarti only", "Visarjan"],
            "answer_index": 0,
            "explanation": "During Kanya Pujan, nine young girls are welcomed, their feet washed, and offered prasad of Puri, Chana, and Halwa."
        },
        {
            "id": "nv6",
            "question": "What majestic predator is Goddess Durga's divine mount (Vahana)?",
            "options": ["The Lion / Tiger (सिंह / बाघ)", "The Elephant", "The Bull", "The Peacock"],
            "answer_index": 0,
            "explanation": "The lion symbolizes fearless power and mastering raw instinct under spiritual wisdom."
        },
        {
            "id": "nv7",
            "question": "What delicious fasting dish prepared from tapioca pearls and roasted peanuts is enjoyed during Navratri fasts?",
            "options": ["Sabudana Khichdi / Vada (साबूदाना खिचड़ी)", "Wheat roti", "Basmati rice", "Moong dal halwa"],
            "answer_index": 0,
            "explanation": "Sabudana Khichdi, Kuttu (buckwheat) puri, and Singhadha flour snacks are popular festive fasting foods."
        },
        {
            "id": "nv8",
            "question": "In West Bengal and East India, what world-renowned grand festival coincides with Navratri?",
            "options": ["Durga Puja (दुर्गा पूजा)", "Kali Puja only", "Rath Yatra", "Pongal"],
            "answer_index": 0,
            "explanation": "Durga Puja features magnificent artistic pandals, Dhunuchi dance, and idol worship celebrated worldwide."
        },
        {
            "id": "nv9",
            "question": "What traditional clay pot with intricate cutouts holding an oil lamp is the centerpiece of Garba dancing?",
            "options": ["Garbo (Garbha Deep / गर्भ दीप)", "Kumbh", "Thali", "Kalash"],
            "answer_index": 0,
            "explanation": "The 'Garbo' pot with an oil lamp symbolizes the universe and the divine spark of life within all beings."
        },
        {
            "id": "nv10",
            "question": "What noble quality does Navratri inspire in every young boy and girl?",
            "options": ["Inner strength, standing up for justice, and deep respect for women", "Being aggressive", "Giving up easily", "Disrespecting nature"],
            "answer_index": 0,
            "explanation": "Navratri teaches us to nurture inner courage, conquer negative habits, and revere the divine feminine."
        }
    ],
    "makar_sankranti": [
        {
            "id": "ms1",
            "question": "Which celestial deity's northward journey (Uttarayana) does Makar Sankranti celebrate?",
            "options": ["Surya Dev (The Sun God / सूर्य देव)", "Chandra Dev (The Moon)", "Varuna Dev", "Indra Dev"],
            "answer_index": 0,
            "explanation": "Makar Sankranti marks the Sun entering Uttarayana, bringing longer sunny days and winter harvest."
        },
        {
            "id": "ms2",
            "question": "What thrilling sky sport fills the horizon with vibrant colors in Gujarat and North India on Sankranti (Uttarayan)?",
            "options": ["Kite Flying (पतंगबाजी)", "Drone racing", "Fireworks", "Parachuting"],
            "answer_index": 0,
            "explanation": "Millions of colorful kites (Patang) take to the winter skies with friendly shouts of 'Kai Po Che!'."
        },
        {
            "id": "ms3",
            "question": "What traditional sweet made of sesame seeds and jaggery is exchanged with the blessing 'Til-Gud khao, meetha bolo'?",
            "options": ["Til-Gud Laddoos and Chikki (तिल-गुड़)", "Jalebi", "Rasgulla", "Modak"],
            "answer_index": 0,
            "explanation": "Til (sesame) provides winter warmth, while Gud (jaggery) represents sweetness in speech and relationships."
        },
        {
            "id": "ms4",
            "question": "In Punjab, what joyous harvest bonfire festival is celebrated on the eve of Makar Sankranti?",
            "options": ["Lohri (लोहड़ी)", "Baisakhi", "Karwa Chauth", "Teej"],
            "answer_index": 0,
            "explanation": "Lohri features dancing Bhangra and Giddha around a cozy bonfire, tossing in sesame, popcorn, and peanuts."
        },
        {
            "id": "ms5",
            "question": "What savory comfort dish made from new rice, lentils, and winter vegetables is eaten in UP, Bihar, and Delhi?",
            "options": ["Khichdi (खिचड़ी)", "Biryani", "Chole Bhature", "Pav Bhaji"],
            "answer_index": 0,
            "explanation": "In Uttar Pradesh and Bihar, the festival is also warmly called 'Khichdi' after this nutritious meal."
        },
        {
            "id": "ms6",
            "question": "Why is Makar Sankranti unique compared to most other Hindu festivals that follow the lunar calendar?",
            "options": ["It follows the solar calendar and almost always falls on January 14th / 15th", "It has no sweets", "It is celebrated at night only", "It happens twice a year"],
            "answer_index": 0,
            "explanation": "Makar Sankranti is one of the few Hindu festivals calculated on solar movements, keeping a consistent date in mid-January."
        },
        {
            "id": "ms7",
            "question": "What sacred holy dip do millions of pilgrims take at the confluence (Sangam) of holy rivers in Prayagraj?",
            "options": ["Holy Snan (पवित्र स्नान at Triveni Sangam)", "Rain shower", "Swimming race", "Boat cruise"],
            "answer_index": 0,
            "explanation": "Pilgrims take an auspicious morning dip at the Sangam of Ganga, Yamuna, and Saraswati during the Magh Mela."
        },
        {
            "id": "ms8",
            "question": "What zodiac sign (Rashi) does the Sun transition into on Makar Sankranti?",
            "options": ["Makara Rashi (Capricorn / मकर राशि)", "Mesha Rashi (Aries)", "Simha Rashi (Leo)", "Kanya Rashi (Virgo)"],
            "answer_index": 0,
            "explanation": "The festival gets its name from the Sun's transit (Sankramana) into the Makara (Capricorn) constellation."
        },
        {
            "id": "ms9",
            "question": "What sweet treat made of puffed rice mixed with hot jaggery is popular in rural North India?",
            "options": ["Lai / Murmura Laddoo (मुरमुरा लड्डू)", "Peda", "Sandesh", "Barfi"],
            "answer_index": 0,
            "explanation": "Crunchy Murmura Laddoos and peanut Chikki are festive winter staples enjoyed across villages and cities."
        },
        {
            "id": "ms10",
            "question": "What noble character lesson does the sharing of Til-Gud sweets teach us?",
            "options": ["Speak sweet, encouraging words to all and dissolve past misunderstandings", "Compete with friends", "Keep the best sweets for yourself", "Stay indoors"],
            "answer_index": 0,
            "explanation": "Til-Gud reminds us to infuse warmth and sweetness into our speech, building lifelong harmonious bonds."
        }
    ],
    "ganesh_chaturthi": [
        {
            "id": "gc1",
            "question": "Whose divine birthday as the Lord of Wisdom and Remover of Obstacles is celebrated on Ganesh Chaturthi?",
            "options": ["Lord Ganesha (Ganpati Bappa / विघ्नहर्ता)", "Lord Shiva", "Lord Vishnu", "Lord Kartikeya"],
            "answer_index": 0,
            "explanation": "Ganesh Chaturthi celebrates the arrival of Lord Ganesha, the elephant-headed deity of intellect and success."
        },
        {
            "id": "gc2",
            "question": "What sweet steamed dumpling filled with fresh grated coconut and jaggery is Lord Ganesha's favorite?",
            "options": ["Modak (मोदक)", "Jalebi", "Gulab Jamun", "Rasgulla"],
            "answer_index": 0,
            "explanation": "Lord Ganesha is fondly offered 21 steamed Ukadiche Modaks, earning him the name 'Modakapriya'."
        },
        {
            "id": "gc3",
            "question": "What humble, observant creature is Lord Ganesha's trusted vehicle (Vahana)?",
            "options": ["Mooshak the Mouse / Rat (मूषकराज)", "The Peacock", "Nandi the Bull", "Garuda"],
            "answer_index": 0,
            "explanation": "Mooshak the mouse symbolizes controlling desire, ego, and navigating through small challenges with agility."
        },
        {
            "id": "gc4",
            "question": "What famous joyful Marathi & Hindi slogan is chanted during Ganesha processions?",
            "options": ["'Ganpati Bappa Morya, Pudhchya Varshi Lavkar Ya!' (गणपति बप्पा मोरया!)", "'Jai Shri Ram!'", "'Har Har Mahadev!'", "'Jai Ho!'"],
            "answer_index": 0,
            "explanation": "Devotees enthusiastically chant praises requesting Bappa to shower blessings and return early next year."
        },
        {
            "id": "gc5",
            "question": "What eco-friendly natural material is best used to make Ganesha idols to protect marine ecosystems?",
            "options": ["Natural Clay / Shadu Mati (शाडू माटी)", "Plastic", "Plaster of Paris with chemicals", "Cement"],
            "answer_index": 0,
            "explanation": "Eco-friendly clay Ganeshas dissolve naturally in water, nurturing aquatic life without chemical pollution."
        },
        {
            "id": "gc6",
            "question": "Which great freedom fighter transformed Ganesh Chaturthi into a grand public community festival in 1893?",
            "options": ["Lokmanya Bal Gangadhar Tilak (लोकमान्य तिलक)", "Mahatma Gandhi", "Bhagat Singh", "Sardar Patel"],
            "answer_index": 0,
            "explanation": "Bal Gangadhar Tilak established the Sarvajanik Ganeshotsav to unite all people in India's freedom struggle."
        },
        {
            "id": "gc7",
            "question": "What sacred green grass blades are specially offered in bunches of 21 to Lord Ganesha during puja?",
            "options": ["Durva Grass (दूर्वा घास)", "Tulsi leaves only", "Neem leaves", "Rose stems"],
            "answer_index": 0,
            "explanation": "Three-bladed green Durva grass is cooling, medicinal, and dearest to Lord Ganesha."
        },
        {
            "id": "gc8",
            "question": "What grand immersion ceremony in rivers, lakes, or home water tubs marks the conclusion of the festival?",
            "options": ["Ganesh Visarjan (गणेश विसर्जन)", "Deepam", "Hawan", "Aarti only"],
            "answer_index": 0,
            "explanation": "Ganesh Visarjan symbolizes that the formless Supreme Divine returns to nature, reminding us of life's eternal cycles."
        },
        {
            "id": "gc9",
            "question": "What do Lord Ganesha's large ears remind every student and young learner to practice?",
            "options": ["Listen patiently, absorb good knowledge, and speak thoughtfully", "Talk over others", "Ignore teachers", "Listen to loud noise"],
            "answer_index": 0,
            "explanation": "Ganesha's large elephant ears symbolize being a great listener, absorbing wisdom, and filtering out negativity."
        },
        {
            "id": "gc10",
            "question": "Why is Lord Ganesha always worshipped first before beginning any new school year, project, or journey?",
            "options": ["He is the Vighnaharta (Remover of all obstacles and blesser of good beginnings)", "He loves celebrations", "He is the oldest deity", "He carries sweets"],
            "answer_index": 0,
            "explanation": "Worshipping Ganesha first blesses our minds with clarity, removing hurdles from our studies and endeavors."
        }
    ],
    "chhath_puja": [
        {
            "id": "cp1",
            "question": "To which primordial deity of cosmic energy, light, and nature is Chhath Puja dedicated?",
            "options": ["Surya Dev (The Sun God) and Chhathi Maiya (सूर्य देव और छठी मइया)", "Lord Indra", "Lord Vayu", "Lord Agni"],
            "answer_index": 0,
            "explanation": "Chhath Puja is an ancient Vedic festival thanking Surya Dev and Chhathi Maiya for sustaining all life on Earth."
        },
        {
            "id": "cp2",
            "question": "In which Indian states is Chhath Puja celebrated with the purest devotion and community spirit?",
            "options": ["Bihar, Jharkhand, Uttar Pradesh, and across the globe", "Punjab only", "Kerala only", "Goa only"],
            "answer_index": 0,
            "explanation": "Chhath is the cultural pride of Bihar, Jharkhand, and UP, celebrated by millions worldwide at water bodies."
        },
        {
            "id": "cp3",
            "question": "What unique traditional Prasad made from whole wheat flour, jaggery, and dry fruits is baked on earthen stoves?",
            "options": ["Thekua (ठेकुआ / खजूरिया)", "Gujiya", "Rasgulla", "Jalebi"],
            "answer_index": 0,
            "explanation": "Thekua, made from stone-ground wheat, jaggery, and ghee with wooden molds, is the sacred Prasad of Chhath."
        },
        {
            "id": "cp4",
            "question": "Where do devotees stand in waist-deep water to offer their Arghya prayers at sunrise and sunset?",
            "options": ["In rivers (Ganga), ponds, lakes, and coastal waters", "Inside dark rooms", "On rooftops only", "In cars"],
            "answer_index": 0,
            "explanation": "Vratis stand in clean natural water bodies, connecting directly with nature and solar rays."
        },
        {
            "id": "cp5",
            "question": "How many days does the rigorous, sacred observance of Chhath Puja span?",
            "options": ["4 Days (Nahay Khay, Kharna, Sandhya Arghya, Usha Arghya)", "1 Day", "2 Days", "7 Days"],
            "answer_index": 0,
            "explanation": "The 4 days include purification (Nahay Khay), fasting (Kharna), evening offering, and morning sunrise Arghya."
        },
        {
            "id": "cp6",
            "question": "What unique philosophical tradition distinguishes Chhath Puja from almost all other sun-worshiping rituals?",
            "options": ["Offering Arghya to the setting Sun (Sandhya) first, recognizing both sunset and sunrise equally", "Prayers at midnight only", "No sun gazing", "Only praying at noon"],
            "answer_index": 0,
            "explanation": "Chhath acknowledges that sunset (conclusion) is as worthy of reverence as sunrise (beginning)."
        },
        {
            "id": "cp7",
            "question": "What handmade bamboo winnowing trays and baskets are used to hold the sacred Prasad offerings?",
            "options": ["Soop (सूप) and Daura (दउरा)", "Plastic bowls", "Metal boxes", "Clay cups only"],
            "answer_index": 0,
            "explanation": "Handwoven bamboo Soop and Daura hold seasonal sugarcane, coconuts, grapefruits, and Thekua."
        },
        {
            "id": "cp8",
            "question": "What tall sweet crop forms a natural canopy over the Ghats during the evening Chhath Arghya?",
            "options": ["Sugarcane stalks (ईख / गन्ना)", "Bamboo poles only", "Palm leaves", "Banana trunk only"],
            "answer_index": 0,
            "explanation": "Fresh green sugarcane stalks tied together form a sacred canopy over the offerings at the riverbank."
        },
        {
            "id": "cp9",
            "question": "Which historic Queen in the Mahabharata performed Chhath Sun worship to overcome adversity?",
            "options": ["Queen Draupadi (द्रौपदी) and Kunti", "Gandhari", "Satyavati", "Kaikeyi"],
            "answer_index": 0,
            "explanation": "Draupadi and Kunti performed Chhath Vrat on the advice of sage Dhaumya to regain their kingdom."
        },
        {
            "id": "cp10",
            "question": "What inspiring eco-friendly message does Chhath Puja teach modern humanity?",
            "options": ["Absolute cleanliness, direct harmony with water bodies, zero artificial waste, and social equality", "Buying fast food", "Using plastic", "Staying disconnected from nature"],
            "answer_index": 0,
            "explanation": "Chhath Puja uses 100% natural, biodegradable offerings, unites all social communities equally, and honors nature."
        }
    ],

    # ------------------ PAN-INDIAN FESTIVALS ------------------
    "diwali": [
        {
            "id": "dw1",
            "question": "What is Diwali famously celebrated as worldwide?",
            "options": ["The Festival of Lights (दीपों का त्योहार)", "The Festival of Colors", "The Festival of Rain", "The Festival of Boats"],
            "answer_index": 0,
            "explanation": "Diwali celebrates the victory of light over darkness, good over evil, and wisdom over ignorance."
        },
        {
            "id": "dw2",
            "question": "Which epic King and Queen returned to Ayodhya on Diwali after 14 years of exile?",
            "options": ["Lord Rama and Sita Devi (भगवान श्रीराम और माता सीता)", "Lord Krishna and Rukmini", "King Harsha and Queen", "King Vikramaditya"],
            "answer_index": 0,
            "explanation": "The citizens of Ayodhya illuminated the entire city with thousands of clay diyas to welcome Lord Rama."
        },
        {
            "id": "dw3",
            "question": "Which Goddess of spiritual wealth, auspiciousness, and light is worshipped on Diwali evening?",
            "options": ["Goddess Lakshmi (माता लक्ष्मी)", "Goddess Kali only", "Goddess Saraswati only", "Goddess Parvati only"],
            "answer_index": 0,
            "explanation": "Families clean their homes, illuminate lamps, and perform Lakshmi Puja to invite peace and prosperity."
        },
        {
            "id": "dw4",
            "question": "What traditional clay oil lamps are placed along windows, thresholds, and balconies during Diwali?",
            "options": ["Diyas (दीये / मिट्टी के दीपक)", "Candles only", "Paper lanterns only", "Neon signs"],
            "answer_index": 0,
            "explanation": "Terracotta Diyas filled with mustard oil or ghee bring an incomparable warm, golden festive glow."
        },
        {
            "id": "dw5",
            "question": "What colorful decorative patterns made with colored powders or flower petals adorn the entrance of homes on Diwali?",
            "options": ["Rangoli (रंगोली)", "Wallpaper", "Mosaic tile", "Chalk numbers"],
            "answer_index": 0,
            "explanation": "Vibrant Rangoli designs at the doorstep welcome guests and Goddess Lakshmi with auspicious warmth."
        },
        {
            "id": "dw6",
            "question": "In South India, what victory of Lord Krishna over a tyrannical demon is celebrated on Naraka Chaturdashi?",
            "options": ["Defeat of demon Narakasura", "Defeat of Ravana", "Defeat of Mahishasura", "Defeat of Kamsa"],
            "answer_index": 0,
            "explanation": "Naraka Chaturdashi celebrates the destruction of demon Narakasura by Lord Krishna and Satyabhama."
        },
        {
            "id": "dw7",
            "question": "What fragrant morning ritual bath with herbal paste and sesame oil is taken on Deepavali morning?",
            "options": ["Ganga Snanam / Abhyanga Snan (औषधीय तेल स्नान)", "Cold shower only", "Swimming", "Spraying perfume"],
            "answer_index": 0,
            "explanation": "Abhyanga Snan with warm sesame oil and herbal ubtan purifies the body and welcomes positive health."
        },
        {
            "id": "dw8",
            "question": "What delicious Indian sweets are exchanged among neighbors and friends during Diwali?",
            "options": ["Laddoos, Kaju Katli, Mysore Pak, and Jalebi", "Bitter chocolate only", "Vegetable salad", "Bread only"],
            "answer_index": 0,
            "explanation": "Exchanging sweet boxes with friends and neighbors spreads warmth, joy, and mutual affection."
        },
        {
            "id": "dw9",
            "question": "On the night of Diwali, on which lunar phase does the festival always fall?",
            "options": ["Kartik Amavasya (The darkest new moon night of the year)", "Pournami (Full moon)", "Ekadashi", "Shukla Paksha"],
            "answer_index": 0,
            "explanation": "Diwali falls on the darkest night of Kartik month, transforming total darkness into dazzling light."
        },
        {
            "id": "dw10",
            "question": "What is the ultimate spiritual takeaway of Diwali for children and families?",
            "options": ["Lighting the inner lamp of kindness, knowledge, and sharing joy with those in need", "Buying the most fireworks", "Staying alone", "Boasting about new clothes"],
            "answer_index": 0,
            "explanation": "Diwali reminds us that even a single small lamp can banish immense darkness—encouraging us to spread kindness and hope."
        }
    ]
}

def get_festivals_for_language(language: str = "Tamil") -> List[Dict[str, Any]]:
    """
    Returns festivals for the selected language, plus Pan-Indian festivals.
    """
    lang_lower = (language or "Tamil").lower()
    return [
        f for f in FESTIVALS_DATA
        if f["language"].lower() == lang_lower or f["language"].lower() == "all"
    ]

def get_festival_by_id(festival_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves a festival by its unique ID.
    """
    fid = (festival_id or "").lower().strip()
    for f in FESTIVALS_DATA:
        if f["id"].lower() == fid:
            return f
    return None

def get_festival_quiz(festival_id: str, language: str = "Tamil") -> List[Dict[str, Any]]:
    """
    Retrieves a 10-question gamified quiz dataset for the festival.
    """
    fid = (festival_id or "").lower().strip()
    if fid in FESTIVALS_QUIZ_DATA:
        return FESTIVALS_QUIZ_DATA[fid]
    
    # Fallback to default
    if "hindi" in (language or "").lower():
        return FESTIVALS_QUIZ_DATA["diwali"]
    elif "telugu" in (language or "").lower():
        return FESTIVALS_QUIZ_DATA["ugadi"]
    elif "malayalam" in (language or "").lower():
        return FESTIVALS_QUIZ_DATA["onam"]
    
    return FESTIVALS_QUIZ_DATA["pongal"]

# Alias for compatibility with api routes
get_festival_quiz_questions = get_festival_quiz

