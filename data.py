import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK with your credentials file
cred = credentials.Certificate('flaskfirebase-7f1ef-firebase-adminsdk-135v6-c10dcd1b4b.json')  # Replace with the path to your credentials file
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# Define the data you want to send to Firestore for 10 entries
data_to_send = [
    {
        'Name': 'Tech Summit 2024',
        'Short Description': 'Explore the latest in technology innovations. Join us for a day filled with tech talks, workshops, and networking opportunities.',
        'Long Description': 'Tech Summit 2024 is a premier event for tech enthusiasts. Dive into the latest innovations, gain insights from industry experts, and connect with like-minded individuals. Don\'t miss this opportunity to stay ahead in the rapidly evolving tech landscape.',
        'Venue': 'Pune Convention Center',
        'Date': '2024-03-15',
        'Time': '9:00 AM - 5:00 PM',
        'Organizer': 'Tech Innovators Association',
        'Image': 'https://example.com/image1.jpg',
        'Link': 'https://example.com/tech-summit-2024',
        'Keywords': 'technology, innovation, networking, workshops'
    },
    {
        'Name': 'Art Exhibition - Colors of Expression',
        'Short Description': 'An eclectic showcase of contemporary art. Immerse yourself in the vibrant world of modern art.',
        'Long Description': 'Colors of Expression invites you to a mesmerizing journey through contemporary art. Experience the diverse expressions of artists worldwide, showcasing their creativity in various mediums.',
        'Venue': 'Pune Art Gallery',
        'Date': '2024-04-02',
        'Time': '11:00 AM - 7:00 PM',
        'Organizer': 'Creative Art Collective',
        'Image': 'https://example.com/image2.jpg',
        'Link': 'https://example.com/art-exhibition-2024',
        'Keywords': 'art, exhibition, contemporary, painting'
    },
    {
        'Name': 'Fitness Workshop - Healthy Living',
        'Short Description': 'Learn practical fitness tips for a healthier lifestyle. Discover the key to a balanced and active life.',
        'Long Description': 'Join us for a Fitness Workshop focused on practical tips for a healthier lifestyle. Our experts will guide you through effective exercises and nutrition strategies, empowering you to lead a more active and balanced life.',
        'Venue': 'Pune Wellness Center',
        'Date': '2024-05-10',
        'Time': '6:30 PM - 8:30 PM',
        'Organizer': 'Health Matters Foundation',
        'Image': 'https://example.com/image3.jpg',
        'Link': 'https://example.com/fitness-workshop-2024',
        'Keywords': 'fitness, workshop, health, lifestyle'
    },
    {
        'Name': 'Music Festival - Harmony Unleashed',
        'Short Description': 'A celebration of diverse musical genres. Join us for a night of musical bliss featuring talented artists across genres.',
        'Long Description': 'Harmony Unleashed is a celebration of musical diversity. Join us for a night filled with soulful performances across various genres, including jazz, rock, classical, and more. Let the harmony resonate through the night!',
        'Venue': 'Pune Amphitheater',
        'Date': '2024-06-18',
        'Time': '7:00 PM - 12:00 AM',
        'Organizer': 'Melody Productions',
        'Image': 'https://example.com/image4.jpg',
        'Link': 'https://example.com/music-festival-2024',
        'Keywords': 'music, festival, harmony, genres'
    },
    {
        'Name': 'Startup Bootcamp - Ignite Ideas',
        'Short Description': 'Empowering aspiring entrepreneurs. Dive into the world of startups.',
        'Long Description': 'Ignite Ideas at Startup Bootcamp is your gateway to the startup world. Empower yourself with insights from successful entrepreneurs, gain funding knowledge, and network with potential collaborators. Take the leap towards entrepreneurial success!',
        'Venue': 'Pune Innovation Hub',
        'Date': '2024-07-05',
        'Time': '10:00 AM - 4:00 PM',
        'Organizer': 'Startup Hub',
        'Image': 'https://example.com/image5.jpg',
        'Link': 'https://example.com/startup-bootcamp-2024',
        'Keywords': 'startup, bootcamp, entrepreneurship, collaboration'
    },
    {
        'Name': 'Culinary Delights - Food Festival',
        'Short Description': 'A gastronomic journey of flavors. Indulge your taste buds in a culinary adventure.',
        'Long Description': 'Embark on a gastronomic journey at the Food Festival. Indulge in diverse cuisines, experience cooking demos, and savor food tastings from renowned chefs. Join us for a feast of flavors!',
        'Venue': 'Pune Food Park',
        'Date': '2024-08-20',
        'Time': '12:00 PM - 9:00 PM',
        'Organizer': 'TasteMasters Society',
        'Image': 'https://example.com/image6.jpg',
        'Link': 'https://example.com/food-festival-2024',
        'Keywords': 'culinary, food festival, flavors, tasting'
    },
    {
        'Name': 'Environmental Symposium - Green Planet',
        'Short Description': 'Promoting sustainability and environmental awareness. Join us for insightful discussions, workshops, and initiatives.',
        'Long Description': 'Green Planet Environmental Symposium aims to create a sustainable future. Join us for insightful discussions, engaging workshops, and initiatives focused on promoting environmental awareness and sustainability.',
        'Venue': 'Pune Eco Center',
        'Date': '2024-09-12',
        'Time': '2:00 PM - 6:00 PM',
        'Organizer': 'EcoWarriors Foundation',
        'Image': 'https://example.com/image7.jpg',
        'Link': 'https://example.com/environmental-symposium-2024',
        'Keywords': 'environment, sustainability, symposium, green planet'
    },
    {
        'Name': 'Fashion Show - Trendsetters Showcase',
        'Short Description': 'Unveiling the latest in fashion trends. Witness a spectacular runway show featuring top designers and emerging talents.',
        'Long Description': 'Trendsetters Showcase Fashion Show unveils the latest trends. Witness a spectacular runway show featuring top designers and emerging talents. Immerse yourself in the fusion of style and creativity.',
        'Venue': 'Pune Fashion Hub',
        'Date': '2024-10-08',
        'Time': '6:00 PM - 10:00 PM',
        'Organizer': 'Vogue Trends',
        'Image': 'https://example.com/image8.jpg',
        'Link': 'https://example.com/fashion-show-2024',
        'Keywords': 'fashion, showcase, trends, runway'
    },
    {
        'Name': 'Science Expo - Innovate Tomorrow',
        'Short Description': 'Showcasing cutting-edge scientific advancements. Explore the world of science through interactive exhibits, demonstrations, and discussions.',
        'Long Description': 'Innovate Tomorrow Science Expo showcases cutting-edge advancements. Explore the world of science through interactive exhibits, demonstrations, and discussions. Inspire the scientist within you!',
        'Venue': 'Pune Science Center',
        'Date': '2024-11-15',
        'Time': '10:00 AM - 6:00 PM',
        'Organizer': 'Science Enthusiasts Society',
        'Image': 'https://example.com/image9.jpg',
        'Link': 'https://example.com/science-expo-2024',
        'Keywords': 'science, expo, innovation, advancements'
    },
    {
        'Name': 'Film Festival - Cinematic Visions',
        'Short Description': 'Celebrating diverse cinematic storytelling. Immerse yourself in a collection of thought-provoking films from around the world.',
        'Long Description': 'Cinematic Visions Film Festival celebrates diverse storytelling. Immerse yourself in a collection of thought-provoking films from around the world. Engage in discussions with filmmakers and fellow cinephiles.',
        'Venue': 'Pune Film Palace',
        'Date': '2024-12-03',
        'Time': '4:00 PM - 11:00 PM',
        'Organizer': 'Cinema Arts Society',
        'Image': 'https://example.com/image10.jpg',
        'Link': 'https://example.com/film-festival-2024',
        'Keywords': 'film, festival, cinematic, storytelling'
    }
]

# Send each entry in data_to_send to Firestore
for entry in data_to_send:
    db.collection('States/MH/CT/PU/EVTS').add(entry)

print('10 entries of data sent to Firestore.')
