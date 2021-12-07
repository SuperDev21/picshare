import sqlite3

DATABASE = 'app.db'
db = sqlite3.connect(DATABASE)

cursor = db.cursor()

# Creation of table "categories". If it existed already, we delete the table and create a new one
cursor.execute('DROP TABLE IF EXISTS categories')
cursor.execute("""CREATE TABLE categories (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name VARCHAR(200) NOT NULL)""")

# We seed the table with initial values. 
# Here we insert 5 categories
for name in ["Landscapes", "Cities", "Animals", "Outdoors", "Portraits"]:
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))

# Creation of table "Images"
cursor.execute("DROP TABLE IF EXISTS images")
cursor.execute("""CREATE TABLE images (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   name VARCHAR(200) ,
                                   img VARCHAR(200) , 
                                   description VARCHAR(200) ,
                                   date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
                                   vote INTEGER,
                                   category_id INTEGER,
                                   CONSTRAINT fk_categories
                                     FOREIGN KEY (category_id)
                                     REFERENCES categories(category_id))""")

# We seed the table with initial values. Here 2 images are inserted into the table "images"
for data in [
        ("Paris", "paris.jpeg", "The tower has three levels for visitors,\
        with restaurants on the first and second levels. The top \
        level's upper platform is 276 m (906 ft) above the ground \
        – the highest observation deck accessible to the public in the \
         European Union.", "2020-07-04", None, 2),
        ("Bird", "oiseau.jpg", "Bird colorful", "2020-03-01", None, 3),
        ("Peacefull cat", "peacefull_cat.jpg", "The best life ever ! eating and being \
        stroked all day long.", "2019-08-12", None, 3),
        ("Orangutan", "orangutan.jpg", "The Orangutan is the largest arboreal mammal. The name \
        orangutan comes from the Malayan orang hutan, which literally means man of the forest.\
        This great ape has taken up residence in the treetops and tirelessly roams the canopy \
        in search of fruits, leaves and insects.", "2019-04-23", None, 3),
        ("American buffalo", "buffalo.jpg", "An american buffalo in the snow - Yellowstone National Park",\
        "2017-12-14", None, 3),
        ("Red Panda", "red_panda.jpg", "Cute red padding laying on tree stump. The Red Panda is a protected \
        mammal in danger of extinction. The red panda is native to the Himalayas and southwestern \
        China and prefers to live in the region's temperate mixed mountain forests, which are\
        rich in bamboo.", "2015-06-06", None, 3),
        ("Peacock", "peacock.jpg", "The remarkable plumage of Peacocks is the reason for their popularity \
        in culture and the arts.", "2020-04-05", None, 3),
        ("Majestic Tiger", "majestic_tiger.jpg", "A fabulous animal that inspired terror and respect \
        for the ancients, the tiger would have disappeared during the 20th century if the world scientific \
        community had not sounded the alarm bells. It was in 1969 that WWF reported the catastrophic \
        numbers of tigers, less than 2,000 in India. Of the 7 subspecies that lived in 1900, \
        only 5 remain today", "2017-01-15", None, 3),
        ("Blue face Toucan", "toucan.jpg", "Prior to 2011, the Swainson's Toucan was elevated to a \
        full species, but it is now considered a simple subspecies of the Tocard Toucan with an \
        orange beak", "2021-02-12", None, 3),
        ("Rhinos", "rhinos.jpg", "Until the middle of the 19th century, rhinos were widely distributed \
        in the savannas of Africa and the tropical forests of Asia. Today, 4 of the 5 rhino species \
        are vulnerable or critically endangered. Their horns, now more prized than gold or cocaine, \
        are their curse", "2019-03-07", None, 3),
        ("Zurich", "zurich.jpg", "Zurich cityscape with a swan on the river Limmat in Switzerland", "2014-05-02", None, 2),
        ("Univertsity of Missouri", "university_missouri.jpg", "The University of Missouri located in Columbia, Missouri", "2015-06-04", None, 2),
        ("Ground Zero", "ground_zero.jpg", "The destroyed Ground Zero of the fallen Twin Towers, New York City, New York", "2010-09-11", None, 2),
        ("Chicago Dowtown", "downtown_chicago.jpg", "Railroad tracks leading to downtown Chicago", "2020-09-19", None, 2),
        ("Philadelphia City", "philadelphia.jpg", "Aerial view of Philadelphia, Pennsylvania", "2020-11-06", None, 2),
        ("Oahu in Hawaii", "oahu.jpg", "Aerial shot of Waikiki Beach, Oahu, Hawaii", "2018-06-07", None, 2),
        ("Capitol", "capitol.jpg", "Capitol Building, Salt Lake City, Utah", "2015-04-15", None, 2),
        ("Lighthouse", "lighthouse.jpg", "Aerial view of the Morris Island Lighthouse in Charleston, South Carolina", "2017-02-18", None, 1),
        ("Church of Mary the Queen", "mary_church.jpg", "The Church of Mary the Queen, also known as the Pilgrimage Church of the Assumption of Mary,\
        or Our Lady of the Lake, is located on a small island in the middle of Lake Bled in Slovenia. The legend says that those who ring the bell and make a wish,\
        will see their wish come true. But there’s one rule: you can make only one wish", "2013-07-18", None, 1),
        ("Autumn pic", "bavarian_alps.jpg", "Autumn scenery near the lake alpsee in the bavarian alps near the german city fussen", "2011-10-08", None, 1),
        ("Bali monochrome", "bali.jpg", "Path in the countryside leading up to an abandoned building in Bali", "2021-03-08", None, 1),
        ("Monument Valley", "monument_valley.jpg", "Scene in the arizona portion of monument valley, a desert region on the arizona-utah\
        border known for the towering sandstone buttes of monument valley navajo tribal park", "2010-08-08", None, 1),
        ("Hong-Kong landscape", "hongkong.jpg", "Lush landscape in Hong Kong with sky, clouds and mountains", "2016-05-11", None, 1),
        ("Rice field", "rice_field.jpg", "Beautiful view of rice paddy field on an over cast day in Cambodgia", "2016-08-20", None, 1),
        ("River", "yellowstone.jpg", "Sunset over river in Yellowstone National Park", "2014-08-19", None, 1),
        ("Winter Road", "winter_road.jpg", "Winter landscape in south germany, near the city of stuttgart with\
        a bicycle alley and a leafless tree covered in frost", "2016-12-15", None, 1),
        ("Winter in mountains", "albuquerque.jpg", "A blustery winter day in the sandia mountains on the\
        north side of albuquerque, new mexico", "2016-11-30", None, 1),
        ("lady smiling", "smile.jpg", "Attractive black women with curly hair and wearing glasses\
        laughing while standing by herself against a gray background", "2018-06-24", None, 5),
        ("Grandma", "old_lady.jpg", "Older female with beautiful smile on her face outdoors in countryside", "2017-07-30", None, 5),
        ("Gothic", "gothic.jpg", "Portrait of a young gothic woman with eyes closed", "2021-01-06", None, 5),
        ("Girl", "little_girl.jpg", "Young happy girl with down syndrome wearing stylish pigtail\
        hairdo and looking down while smiling, grey background", "2016-09-17", None, 5),
        ("Drag Queen", "dragqueen.jpg", "Man dressed as woman looking away with his arms crossed", "2019-10-06", None, 5),
        ("Lollipop", "candy.jpg", "Korean woman holding a big swirl lollipop in front of her face against blue background",\
        "2018-09-18", None, 5),
        ("Mae C. Jemison", "nasa.jpg", "Official nasa portrait of the first black woman in space dr. mae c. jemison", "2021-02-10", None, 5),
        ("Barber", "barber.jpg", "happy barber smiling in barbershop", "2020-02-15", None, 5)
    ]:
    if data[-2] is None:
        cursor.execute("INSERT INTO images (name, img, description, date, vote, category_id) VALUES (?, ?, ?, ?, ?, ?)", data[0:6])
    else:
        cursor.execute("INSERT INTO images (name, img, description, date, vote, category_id) VALUES (?, ?, ?, ?, ?, ?)", data)


# Creation of table "votes". If it existed already, we delete the table and create a new one
cursor.execute('DROP TABLE IF EXISTS votes')
cursor.execute("""CREATE TABLE votes (
                                        vote INTEGER NOT NULL, 
                                        image_id INTEGER NOT NULL,
                                        category_id INTERGER NOT NULL,
                                        CONSTRAINT fk_images
                                        FOREIGN KEY (image_id)
                                        REFERENCES images(image_id)
                                        )""")

# # We seed the table with initial values. 
# # Here we insert 3 categories: "Videogames", "Boardgames" and "Outdoors"
# for data in ["Landscapes", "Cities", "Animals", "Outdoors", "Portraits"]:
#         cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))

# Creation of table "comments". If it existed already, we delete the table and create a new one
cursor.execute('DROP TABLE IF EXISTS comments')
cursor.execute("""CREATE TABLE comments (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                        author VARCHAR(200), 
                                        text VARCHAR(200),
                                        image_id INTEGER,
                                        category_id INTEGER,
                                        CONSTRAINT fk_images
                                        FOREIGN KEY (image_id)
                                        REFERENCES images(image_id)
                                        )""")

# # We seed the table with initial values. 
# # Here we insert 3 comments
for data in [
              ("Nawal", "The tower is 324 metres (1,063 ft) tall, about the same height\
              as an 81-storey building, and the tallest structure in Paris. Its base \
              is square, measuring 125 metres (410 ft) on each side.", 1, 2),
              ("Nelson", "The tower is 324 metres (1,063 ft) tall, about the same height\
              as an 81-storey building, and the tallest structure in Paris.", 1, 2),
              ("Gaëlle", "The tallest structure in Paris.", 1, 2),
              ("Sandrine", "What a face ! beautiful bird", 9, 3),
              ("Caro", "I love the amazing plumage colors", 7, 3),
              ("Erwan", "My brother is a Hipster and he looks like this man", 35, 5),
              ("Jasmine", "I love the 3 piercings aligned with the center of the mouth. It's chic and understated.", 30, 5),
              ("Tom", "Nice Pic ! a little bit scary maybe", 21, 1),
              ("Sven", "The best years of my life were in Chicago. Go bulls!", 14, 2),
              ("Claire", "I imagine how hard that woman had to fight to get to this.", 34, 5)
             ]:


        if data[-2] is None:
                cursor.execute("INSERT INTO comments (author, text, image_id , category_id) VALUES (?, ?, ?, ?)", data[0:4])
        else:
                cursor.execute("INSERT INTO comments (author, text, image_id , category_id) VALUES (?, ?, ?, ?)", data)


# We save our changes into the database file
db.commit()

# We close the connection to the database
db.close()
