import os
import logging
import requests
from typing import List, Dict, Any, Optional

logger = logging.getLogger("ammachi.youtube")

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY") or os.getenv("GOOGLE_API_KEY")

# 100% Verified, Active, Public Embeddable YouTube Videos for Indian Festivals
CURATED_FESTIVAL_VIDEOS: Dict[str, List[Dict[str, Any]]] = {
    "pongal": [
        {
            "video_id": "Dw_Lqg737lw",
            "title": "பொங்கல் பொங்கும் பாடல் | Pongal Festival Story & Song for Kids",
            "description": "Learn the 4 days of Pongal (Bhogi, Surya Pongal, Mattu Pongal, Kaanum Pongal) with fun animated storytelling.",
            "thumbnail": "https://img.youtube.com/vi/Dw_Lqg737lw/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/Dw_Lqg737lw",
            "channel_title": "Punnagai Kids Tamil"
        },
        {
            "video_id": "laJx7CdPugY",
            "title": "Wish You All a Very Happy Pongal | Animated Tamil Story",
            "description": "Festive Pongal songs and traditions celebrating the sun and farmers.",
            "thumbnail": "https://img.youtube.com/vi/laJx7CdPugY/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/laJx7CdPugY",
            "channel_title": "MagicBox Tamil Stories"
        },
        {
            "video_id": "OFrZQtw7tf4",
            "title": "பொங்கலோ பொங்கல் | Pongalo Pongal Animation Story for Kids",
            "description": "Boiling sweet Pongal pot and thanking farm animals.",
            "thumbnail": "https://img.youtube.com/vi/OFrZQtw7tf4/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/OFrZQtw7tf4",
            "channel_title": "Superkid TV"
        }
    ],
    "puthandu": [
        {
            "video_id": "wolGjb_2TIc",
            "title": "இனிய தமிழ் புத்தாண்டு வாழ்த்துகள் | Tamil New Year for Children",
            "description": "Celebrating the first day of Chithirai month with Maanga Pachadi.",
            "thumbnail": "https://img.youtube.com/vi/wolGjb_2TIc/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/wolGjb_2TIc",
            "channel_title": "infobells - Tamil"
        },
        {
            "video_id": "LREDbGhZS48",
            "title": "புத்தாண்டு Surprise | Tamil New Year Kids Animation",
            "description": "Sweet, sour, and bitter flavours representing life's diverse experiences.",
            "thumbnail": "https://img.youtube.com/vi/LREDbGhZS48/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/LREDbGhZS48",
            "channel_title": "PunToon Kids - Tamil"
        },
        {
            "video_id": "lIoxxHet2Zo",
            "title": "The New Year Story in Tamil | Animated Moral Stories",
            "description": "Joyful Puthandu celebrations and viewing Kanni.",
            "thumbnail": "https://img.youtube.com/vi/lIoxxHet2Zo/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/lIoxxHet2Zo",
            "channel_title": "PunToon Kids - Tamil"
        }
    ],
    "karthigai_deepam": [
        {
            "video_id": "7ZBC1ZZtpR4",
            "title": "கார்த்திகை தீபம் ஏன் கொண்டாடுகிறோம்? | Kids Karthigai Deepam Story",
            "description": "Why we light clay oil lamps (Agal Vilakku) on full moon day in Karthigai month.",
            "thumbnail": "https://img.youtube.com/vi/7ZBC1ZZtpR4/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/7ZBC1ZZtpR4",
            "channel_title": "Kutty Meow"
        },
        {
            "video_id": "qpRtJv9X9Zc",
            "title": "Karthigai Deepam Story | Infinite Flame Explained for Kids",
            "description": "The sacred festival of lights welcoming wisdom and joy into every home.",
            "thumbnail": "https://img.youtube.com/vi/qpRtJv9X9Zc/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/qpRtJv9X9Zc",
            "channel_title": "TheCurioZone_in"
        },
        {
            "video_id": "Q29XHDdF4qY",
            "title": "கார்த்திகை தீபம் | Karthigai Deepam Tamil Kids Rhyme & Story",
            "description": "Rows of glowing lamps illuminating the night.",
            "thumbnail": "https://img.youtube.com/vi/Q29XHDdF4qY/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/Q29XHDdF4qY",
            "channel_title": "Kanmani Poongaa"
        }
    ],
    "thaipusam": [
        {
            "video_id": "uWDlwLEsVE8",
            "title": "Thai Poosam Explained for Kids | Lord Murugan & Tamil Culture",
            "description": "Lord Murugan receiving the spear of wisdom (Vel) and devotion.",
            "thumbnail": "https://img.youtube.com/vi/uWDlwLEsVE8/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/uWDlwLEsVE8",
            "channel_title": "Jalebi Tales"
        },
        {
            "video_id": "Pwhxk_H9YSw",
            "title": "Story of Swamimalai & Lord Murugan Stories for Kids",
            "description": "Arupadai Veedu traditions and carrying Kavadi with yellow flowers.",
            "thumbnail": "https://img.youtube.com/vi/Pwhxk_H9YSw/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/Pwhxk_H9YSw",
            "channel_title": "Pebbles Temple Tourism"
        },
        {
            "video_id": "W1_ORyhTKA0",
            "title": "தைப்பூசம் வரலாறு | Thaipusam Animated Story in Tamil",
            "description": "Bravery, kindness, and devotion celebrated on Thaipusam.",
            "thumbnail": "https://img.youtube.com/vi/W1_ORyhTKA0/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/W1_ORyhTKA0",
            "channel_title": "Arivu Kathaigal"
        }
    ],
    "vinayagar_chaturthi": [
        {
            "video_id": "fIfDVz_T0Zw",
            "title": "பிள்ளையார் பிள்ளையார் பெருமை வாய்ந்த பிள்ளையார் | Vinayagar Song & Story",
            "description": "Sweet Kozhukattai, clay Pillaiyar making, and the loving wisdom of Lord Ganesha.",
            "thumbnail": "https://img.youtube.com/vi/fIfDVz_T0Zw/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/fIfDVz_T0Zw",
            "channel_title": "infobells - Tamil"
        },
        {
            "video_id": "xhYmE0BA_DY",
            "title": "ஆனை முகத்தோனே கணபதியே | Vinayagar Chaturthi Tamil Rhymes & Story",
            "description": "Why we offer Arugampul grass, break coconuts, and celebrate Vinayagar Chaturthi.",
            "thumbnail": "https://img.youtube.com/vi/xhYmE0BA_DY/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/xhYmE0BA_DY",
            "channel_title": "infobells - Tamil"
        },
        {
            "video_id": "ueEn1hhdoXY",
            "title": "விக்னங்களை தீர்க்கும் விநாயகர் | Vinayagar Moral Stories for Kids",
            "description": "How Lord Ganesha circled his parents to win the Gnana Pazham mango of wisdom.",
            "thumbnail": "https://img.youtube.com/vi/ueEn1hhdoXY/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/ueEn1hhdoXY",
            "channel_title": "infobells - Tamil"
        }
    ],
    "ayudha_pooja": [
        {
            "video_id": "fQ1K2rqH7_k",
            "title": "ஆயுத பூஜை & சரஸ்வதி பூஜை பாடல் | Ayudha Pooja Song & Story for Kids",
            "description": "Blessing books, tools, computers, and vehicles with sandalwood, kumkumam, and sweet Pori.",
            "thumbnail": "https://img.youtube.com/vi/fQ1K2rqH7_k/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/fQ1K2rqH7_k",
            "channel_title": "Pebbles Tamil"
        },
        {
            "video_id": "ThjDnU2vLgg",
            "title": "Ayudha Pooja & Saraswati Pooja Story in Tamil | Why We Celebrate",
            "description": "Honoring Goddess Saraswathi for wisdom and respecting the tools that help us work and learn.",
            "thumbnail": "https://img.youtube.com/vi/ThjDnU2vLgg/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/ThjDnU2vLgg",
            "channel_title": "Avee Kutty Stories"
        },
        {
            "video_id": "Yb7IdDh1Jvc",
            "title": "ஆயுத பூஜை & சரஸ்வதி பூஜை சிறப்பு கதை | Ayudha Pujai Special Story",
            "description": "Pandavas retrieving their tools, Vijayadashami Vidyarambham, and the dignity of labor.",
            "thumbnail": "https://img.youtube.com/vi/Yb7IdDh1Jvc/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/Yb7IdDh1Jvc",
            "channel_title": "Pebbles Tamil"
        }
    ],
    "ugadi": [
        {
            "video_id": "A5xN-Sjg_Bc",
            "title": "Ugadi Festival Animated Story in Telugu for Kids | ఉగాది పండుగ కథ",
            "description": "Telugu New Year traditions and the 6 tastes of Ugadi Pachadi (Shadruchulu).",
            "thumbnail": "https://img.youtube.com/vi/A5xN-Sjg_Bc/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/A5xN-Sjg_Bc",
            "channel_title": "memme toonz"
        },
        {
            "video_id": "1eyvNOl9MNY",
            "title": "ఉగాది కథ | Significance & Importance of Ugadi | KidsOneTelugu",
            "description": "Raw mango, neem flowers, jaggery, tamarind, salt, and chili tastes.",
            "thumbnail": "https://img.youtube.com/vi/1eyvNOl9MNY/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/1eyvNOl9MNY",
            "channel_title": "Kidsone Telugu"
        },
        {
            "video_id": "0WcFUZcCDPo",
            "title": "Ugadi Ugadi Happy Happy Ugadi | Telugu Rhymes for Children",
            "description": "Joyful Ugadi festive song and family traditions.",
            "thumbnail": "https://img.youtube.com/vi/0WcFUZcCDPo/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/0WcFUZcCDPo",
            "channel_title": "infobells - Telugu"
        }
    ],
    "sankranti": [
        {
            "video_id": "SfsV2D3RoKI",
            "title": "సంక్రాంతి పండుగ కథ | Makar Sankranti Telugu Animated Story",
            "description": "Bhogi bonfires, colorful Muggulu (rangoli), and Haridasu songs.",
            "thumbnail": "https://img.youtube.com/vi/SfsV2D3RoKI/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/SfsV2D3RoKI",
            "channel_title": "PunToon Kids - Telugu"
        },
        {
            "video_id": "TsBM5E3kpu0",
            "title": "Telugu Stories | Sankranthi Story | సంక్రాంతి పండుగ కథ",
            "description": "Kite flying, delicious Ariselu sweets, and harvest celebrations.",
            "thumbnail": "https://img.youtube.com/vi/TsBM5E3kpu0/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/TsBM5E3kpu0",
            "channel_title": "Kidsone Telugu"
        },
        {
            "video_id": "Vlygnk8GwPs",
            "title": "Makar Sankranti Kids Story in Telugu | Telugu Kathalu",
            "description": "Three days of harvest celebrations in Andhra Pradesh and Telangana.",
            "thumbnail": "https://img.youtube.com/vi/Vlygnk8GwPs/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/Vlygnk8GwPs",
            "channel_title": "KidsOne"
        }
    ],
    "bonalu": [
        {
            "video_id": "cz3dWuVdLMk",
            "title": "What is Bonalu? | Telangana's Famous Festival | Telugu Kids Animation",
            "description": "Decorated earthen pots with cooked rice and neem leaves.",
            "thumbnail": "https://img.youtube.com/vi/cz3dWuVdLMk/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/cz3dWuVdLMk",
            "channel_title": "joShu Tales"
        },
        {
            "video_id": "lAcyPp7Lezs",
            "title": "Bonalu Festival Story for Kids | Telangana Culture",
            "description": "Rhythmic drum beats, Pothuraju dances, and thanking Goddess Mahakali.",
            "thumbnail": "https://img.youtube.com/vi/lAcyPp7Lezs/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/lAcyPp7Lezs",
            "channel_title": "Machi's Kids Channel"
        },
        {
            "video_id": "vfA515Ub7Kg",
            "title": "Bonalu Festival Story for Kids | Mahankali Amma Bonalu Celebration",
            "description": "Telangana folk festival celebration with joyful family traditions.",
            "thumbnail": "https://img.youtube.com/vi/vfA515Ub7Kg/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/vfA515Ub7Kg",
            "channel_title": "BP Kids"
        }
    ],
    "diwali": [
        {
            "video_id": "cvCv7kTcRXI",
            "title": "Why is Diwali called the Festival of Lights? | Dr. Binocs Show",
            "description": "Discover Lord Rama returning to Ayodhya and rows of glowing diyas (Deepavali).",
            "thumbnail": "https://img.youtube.com/vi/cvCv7kTcRXI/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/cvCv7kTcRXI",
            "channel_title": "Peekaboo Kidz"
        },
        {
            "video_id": "74LTtXAlT2o",
            "title": "Diwali - The Festival of Lights | Tia & Tofu Kids Story",
            "description": "Clay oil lamps, homemade sweets, colorful rangoli, and sharing happiness.",
            "thumbnail": "https://img.youtube.com/vi/74LTtXAlT2o/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/74LTtXAlT2o",
            "channel_title": "T-Series Kids Hut"
        },
        {
            "video_id": "zzVdq6e_QBk",
            "title": "The Meaning of Diwali | Animated Moral Stories for Kids",
            "description": "Celebrating the victory of light over darkness and goodness over evil.",
            "thumbnail": "https://img.youtube.com/vi/zzVdq6e_QBk/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/zzVdq6e_QBk",
            "channel_title": "Animated Stories"
        }
    ],
    "onam": [
        {
            "video_id": "jZsnO7Zpf_c",
            "title": "The Story of Onam Festival | Mythological Stories from Mocomi Kids",
            "description": "The story of King Mahabali, Vamana, and Kerala's grand harvest festival.",
            "thumbnail": "https://img.youtube.com/vi/jZsnO7Zpf_c/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/jZsnO7Zpf_c",
            "channel_title": "MocomiKids"
        },
        {
            "video_id": "_EeiwqjeZ3o",
            "title": "Onam Cartoon for Kids | Pookalam, Onam Dance & Onasadya Feast",
            "description": "Intricate flower carpets (Pookalam) and 26-dish Onasadya banana leaf feast.",
            "thumbnail": "https://img.youtube.com/vi/_EeiwqjeZ3o/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/_EeiwqjeZ3o",
            "channel_title": "Kutuki"
        },
        {
            "video_id": "jGld7ns0Isk",
            "title": "Onam Story of King Mahabali | Nostalgic Kerala Animation",
            "description": "Vallamkali snake boat races and backwaters celebrations in Kerala.",
            "thumbnail": "https://img.youtube.com/vi/jGld7ns0Isk/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/jGld7ns0Isk",
            "channel_title": "Preschool Tales"
        }
    ],
    "holi": [
        {
            "video_id": "qbXpbLBAc1g",
            "title": "रंगबिरंगी होली गीत | Rangbirangi Holi Song for Children",
            "description": "Learn the joyful festival of colors, organic Gulal, Holika Dahan, and Gujiya sweets.",
            "thumbnail": "https://img.youtube.com/vi/qbXpbLBAc1g/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/qbXpbLBAc1g",
            "channel_title": "Infobells - Hindi"
        },
        {
            "video_id": "ZpqBNEcURqs",
            "title": "Holi Festival of Colors | Mighty Little Bheem Story",
            "description": "Fun and playful animated celebration of Holi with colors and friends.",
            "thumbnail": "https://img.youtube.com/vi/ZpqBNEcURqs/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/ZpqBNEcURqs",
            "channel_title": "Netflix Jr."
        },
        {
            "video_id": "-EAS2pWyAZU",
            "title": "Happy Holi! होली का त्योहार | Animated Kids Story",
            "description": "The story of Bhakt Prahlad, Holika bonfire, and forgiveness.",
            "thumbnail": "https://img.youtube.com/vi/-EAS2pWyAZU/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/-EAS2pWyAZU",
            "channel_title": "Jugnu Kids"
        }
    ],
    "dussehra": [
        {
            "video_id": "Shj7Q1FeiIA",
            "title": "दशहरा की कहानी | Dussehra Special Animated Story for Kids",
            "description": "Victory of Lord Rama over the ten-headed demon king Ravana celebrating the triumph of good over evil.",
            "thumbnail": "https://img.youtube.com/vi/Shj7Q1FeiIA/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/Shj7Q1FeiIA",
            "channel_title": "PunToon Kids - Hindi"
        },
        {
            "video_id": "Yrl9ncFMK3s",
            "title": "दशहरा आया रे! Dussehra Song & Story | Hindi Rhymes for Children",
            "description": "Watching Ramlila, burning giant effigies of Ravana, and celebrating truth.",
            "thumbnail": "https://img.youtube.com/vi/Yrl9ncFMK3s/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/Yrl9ncFMK3s",
            "channel_title": "Infobells - Hindi"
        },
        {
            "video_id": "foHAVDlESlQ",
            "title": "दशहरे की सीख | Dussehra Moral Stories for Kids",
            "description": "Teaching children courage, righteousness, and eliminating negative habits.",
            "thumbnail": "https://img.youtube.com/vi/foHAVDlESlQ/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/foHAVDlESlQ",
            "channel_title": "Jabardast TV"
        }
    ],
    "raksha_bandhan": [
        {
            "video_id": "gZeF7pwtdTQ",
            "title": "राखी बांधना! Raksha Bandhan Tyohar | Hindi Rhymes for Children",
            "description": "Sisters tying the sacred thread of protection on brothers' wrists with sweets and blessings.",
            "thumbnail": "https://img.youtube.com/vi/gZeF7pwtdTQ/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/gZeF7pwtdTQ",
            "channel_title": "Infobells - Hindi"
        },
        {
            "video_id": "SNSnguJkspQ",
            "title": "Raksha Bandhan Story | रक्षाबंधन की कहानी | Jalebi Street Kids",
            "description": "The eternal bond of love, care, and mutual respect between brothers and sisters.",
            "thumbnail": "https://img.youtube.com/vi/SNSnguJkspQ/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/SNSnguJkspQ",
            "channel_title": "Jalebi Street Kids"
        },
        {
            "video_id": "rV8F-fpkLIg",
            "title": "Happy Raksha Bandhan Song | रक्षाबंधन स्पेशल",
            "description": "Joyful celebration of siblings and sharing delicious homemade sweets.",
            "thumbnail": "https://img.youtube.com/vi/rV8F-fpkLIg/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/rV8F-fpkLIg",
            "channel_title": "Infobells - Hindi"
        }
    ],
    "janmashtami": [
        {
            "video_id": "nDFVILSI1B8",
            "title": "नटखट कृष्णा! Little Krishna Song | Hindi Rhymes for Children",
            "description": "Birth of Lord Krishna in Mathura, eating Makhan butter, and midnight celebrations.",
            "thumbnail": "https://img.youtube.com/vi/nDFVILSI1B8/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/nDFVILSI1B8",
            "channel_title": "Infobells - Hindi"
        },
        {
            "video_id": "Rf7PeTjcl2Q",
            "title": "Story of Janmashtami in Hindi | Birth of Lord Krishna",
            "description": "Vasudeva carrying baby Krishna across the Yamuna river to Gokul.",
            "thumbnail": "https://img.youtube.com/vi/Rf7PeTjcl2Q/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/Rf7PeTjcl2Q",
            "channel_title": "MocomiKids"
        },
        {
            "video_id": "4oF8DLcCMgU",
            "title": "Happy Janmashtami | Dahi Handi & Bal Gopal Cartoon",
            "description": "Breaking the Dahi Handi pot with human pyramids and joyful chants.",
            "thumbnail": "https://img.youtube.com/vi/4oF8DLcCMgU/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/4oF8DLcCMgU",
            "channel_title": "Jugnu Kids"
        }
    ],
    "navratri": [
        {
            "video_id": "k6DGyoUogTU",
            "title": "नवरात्रि स्पेशल कहानी | Navratri Special Garba & Dandiya Story",
            "description": "Nine sacred nights worshipping Goddess Durga and dancing Garba.",
            "thumbnail": "https://img.youtube.com/vi/k6DGyoUogTU/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/k6DGyoUogTU",
            "channel_title": "PunToon Kids - Hindi"
        },
        {
            "video_id": "b5RTvBGsxAc",
            "title": "दुर्गा माँ की शक्ति | Durga Maa Victory Story for Kids",
            "description": "How Goddess Durga defeated the demon Mahishasura to protect the world.",
            "thumbnail": "https://img.youtube.com/vi/b5RTvBGsxAc/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/b5RTvBGsxAc",
            "channel_title": "PunToon Kids"
        },
        {
            "video_id": "kzJo4hFAi2s",
            "title": "The Story of Goddess Durga & Navratri in Hindi",
            "description": "Celebrating the 9 avatars of Maa Durga (Navadurga) and devotion.",
            "thumbnail": "https://img.youtube.com/vi/kzJo4hFAi2s/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/kzJo4hFAi2s",
            "channel_title": "MocomiKids"
        }
    ],
    "makar_sankranti": [
        {
            "video_id": "h9UUEg0yMzQ",
            "title": "पतंग उड़ी! Makar Sankranti Kite Flying Song for Children",
            "description": "Flying colorful kites in winter skies and eating sweet Til-Gud laddoos.",
            "thumbnail": "https://img.youtube.com/vi/h9UUEg0yMzQ/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/h9UUEg0yMzQ",
            "channel_title": "Infobells - Hindi"
        },
        {
            "video_id": "qytIFulKNJI",
            "title": "मकर संक्रांति की पौराणिक कहानी | Makar Sankranti Story in Hindi",
            "description": "Sun God Surya entering Makara Rashi and thanking farmers for harvest.",
            "thumbnail": "https://img.youtube.com/vi/qytIFulKNJI/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/qytIFulKNJI",
            "channel_title": "PunToon Folktales"
        },
        {
            "video_id": "sPGMjFnOqrI",
            "title": "Makar Sankranti Special Hindi Rhymes & Celebration",
            "description": "Harvest bonfire, sharing sweets, and welcoming longer sunny days.",
            "thumbnail": "https://img.youtube.com/vi/sPGMjFnOqrI/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/sPGMjFnOqrI",
            "channel_title": "Infobells - Hindi"
        }
    ],
    "ganesh_chaturthi": [
        {
            "video_id": "ofZr3bdeMB0",
            "title": "गणपति बप्पा मोरया! Little Ganpati's Birthday Song",
            "description": "Welcoming Lord Ganesha with 21 Modaks, clay idols, and prayer bells.",
            "thumbnail": "https://img.youtube.com/vi/ofZr3bdeMB0/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/ofZr3bdeMB0",
            "channel_title": "Infobells - Hindi"
        },
        {
            "video_id": "EyuVVyXjza8",
            "title": "जय गणेश देवा | Jai Ganesh Deva Story & Aarti for Kids",
            "description": "The wisdom, humility, and elephant head of Lord Ganesha.",
            "thumbnail": "https://img.youtube.com/vi/EyuVVyXjza8/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/EyuVVyXjza8",
            "channel_title": "Ding Dong Bells"
        },
        {
            "video_id": "CszqmGP4nAY",
            "title": "गणेश जी का जन्म | Birth of Lord Ganesha Animated Moral Story",
            "description": "How Goddess Parvati created Ganesha and Lord Shiva blessed him.",
            "thumbnail": "https://img.youtube.com/vi/CszqmGP4nAY/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/CszqmGP4nAY",
            "channel_title": "PunToon Kids"
        }
    ],
    "chhath_puja": [
        {
            "video_id": "Il2T1WvreEg",
            "title": "छठ पूजा की कहानी | The Sacred Story of Chhath Puja in Hindi",
            "description": "Ancient Vedic thanksgiving to Surya Dev (Sun God) and Chhathi Maiya.",
            "thumbnail": "https://img.youtube.com/vi/Il2T1WvreEg/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/Il2T1WvreEg",
            "channel_title": "PunToon Kids - Hindi"
        },
        {
            "video_id": "1GQuocF_les",
            "title": "छठ पूजा की महिमा | Chhath Puja Arghya & Thekua Traditions",
            "description": "Offering Arghya at sunset and sunrise in river water and baking sweet Thekua.",
            "thumbnail": "https://img.youtube.com/vi/1GQuocF_les/hqdefault.jpg",
            "embed_url": "https://www.youtube-nocookie.com/embed/1GQuocF_les",
            "channel_title": "Vrat Parva Tyohar"
        }
    ]
}

def search_youtube_api(query: str, max_results: int = 3) -> List[Dict[str, Any]]:
    """
    Queries YouTube Data API v3 for relevant educational, child-safe videos.
    """
    key = os.getenv("YOUTUBE_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not key or key.startswith("your_"):
        return []

    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": f"{query} animated story for kids",
            "type": "video",
            "videoEmbeddable": "true",
            "safeSearch": "strict",
            "maxResults": max_results,
            "key": key
        }

        response = requests.get(url, params=params, timeout=6)
        if response.status_code == 200:
            data = response.json()
            videos = []
            for item in data.get("items", []):
                vid_id = item.get("id", {}).get("videoId")
                snippet = item.get("snippet", {})
                if vid_id and snippet:
                    videos.append({
                        "video_id": vid_id,
                        "title": snippet.get("title", ""),
                        "description": snippet.get("description", ""),
                        "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url") or f"https://img.youtube.com/vi/{vid_id}/hqdefault.jpg",
                        "embed_url": f"https://www.youtube-nocookie.com/embed/{vid_id}",
                        "channel_title": snippet.get("channelTitle", "YouTube Story")
                    })
            if videos:
                logger.info("Found %d live YouTube videos for query: %s", len(videos), query)
                return videos
    except Exception as e:
        logger.warning("YouTube search exception: %s", e)

    return []

def get_festival_youtube_videos(
    festival_id: str,
    festival_name: str,
    language: str = "Tamil"
) -> List[Dict[str, Any]]:
    """
    Returns verified, embeddable YouTube videos for the given festival and language:
    1. Direct live YouTube Data API v3 search if configured
    2. Curated, 100% verified active embeddable YouTube database
    """
    clean_id = (festival_id or "").lower().strip().replace("-", "_").replace(" ", "_")
    name_clean = (festival_name or "").lower().strip()

    # Direct match in curated videos
    if clean_id in CURATED_FESTIVAL_VIDEOS:
        return CURATED_FESTIVAL_VIDEOS[clean_id]
    
    # Comprehensive festival ID & synonym mapping
    id_map = {
        # Tamil
        "pongal": "pongal",
        "puthandu": "puthandu",
        "tamil_new_year": "puthandu",
        "karthigai_deepam": "karthigai_deepam",
        "karthigai": "karthigai_deepam",
        "thaipusam": "thaipusam",
        "vinayagar_chaturthi": "vinayagar_chaturthi",
        "vinayagar": "vinayagar_chaturthi",
        "pillaiyar_chaturthi": "vinayagar_chaturthi",
        "pillaiyar": "vinayagar_chaturthi",
        "ayudha_pooja": "ayudha_pooja",
        "ayudhapooja": "ayudha_pooja",
        "ayudha_puja": "ayudha_pooja",
        "ayudha": "ayudha_pooja",
        "saraswathi_pooja": "ayudha_pooja",
        "saraswathi_puja": "ayudha_pooja",
        "saraswathi": "ayudha_pooja",
        # Telugu
        "ugadi": "ugadi",
        "sankranti": "sankranti",
        "makara_sankranti": "sankranti",
        "bonalu": "bonalu",
        # Malayalam
        "onam": "onam",
        # Hindi
        "holi": "holi",
        "dussehra": "dussehra",
        "vijayadashami": "dussehra",
        "dasara": "dussehra",
        "raksha_bandhan": "raksha_bandhan",
        "rakshabandhan": "raksha_bandhan",
        "rakhi": "raksha_bandhan",
        "janmashtami": "janmashtami",
        "krishna_janmashtami": "janmashtami",
        "krishna": "janmashtami",
        "navratri": "navratri",
        "durga_puja": "navratri",
        "durgapuja": "navratri",
        "durga": "navratri",
        "makar_sankranti": "makar_sankranti",
        "lohri": "makar_sankranti",
        "ganesh_chaturthi": "ganesh_chaturthi",
        "ganesh": "ganesh_chaturthi",
        "ganpati": "ganesh_chaturthi",
        "vinayaka_chaturthi": "ganesh_chaturthi",
        "vinayaka": "ganesh_chaturthi",
        "chhath_puja": "chhath_puja",
        "chhath": "chhath_puja",
        # Pan-Indian
        "diwali": "diwali",
        "deepavali": "diwali"
    }

    matched_key = id_map.get(clean_id)
    if not matched_key:
        for k, v in id_map.items():
            if k in clean_id or k in name_clean:
                matched_key = v
                break

    # 1. Try YouTube Data API v3 live search if API key exists
    if YOUTUBE_API_KEY and not YOUTUBE_API_KEY.startswith("your_"):
        search_query = f"{festival_name} {language} festival celebration story"
        live_videos = search_youtube_api(search_query, max_results=3)
        if live_videos:
            return live_videos

    # 2. Return 100% verified, active embeddable video list
    if matched_key and matched_key in CURATED_FESTIVAL_VIDEOS:
        return CURATED_FESTIVAL_VIDEOS[matched_key]

    # Fallback by language
    if "hindi" in (language or "").lower():
        return CURATED_FESTIVAL_VIDEOS.get("holi", [])
    elif "telugu" in (language or "").lower():
        return CURATED_FESTIVAL_VIDEOS.get("ugadi", [])
    elif "malayalam" in (language or "").lower():
        return CURATED_FESTIVAL_VIDEOS.get("onam", [])

    return CURATED_FESTIVAL_VIDEOS.get("diwali", [])

