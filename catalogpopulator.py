# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catalogDB import Base, Cities, Items, User

# connecting to database
engine = create_engine('sqlite:///citiesfinal.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# fill in the cities with their names
istanbul = Cities(name="Istanbul")
session.add(istanbul)
moscow = Cities(name="Moscow")
session.add(moscow)
london = Cities(name="London")
session.add(london)
petersburg = Cities(name="St. Petersburg")
session.add(petersburg)
berlin = Cities(name="Berlin")
session.add(berlin)
madrid = Cities(name="Madrid")
session.add(madrid)
kiew = Cities(name="Kiew")
session.add(kiew)
rome = Cities(name="Rome")
session.add(rome)
paris = Cities(name="Paris")
session.add(paris)
minsk = Cities(name="Minsk")
session.add(minsk)

# fill in the attractions with their names, descriptions and city-ids
hagia_sophia = Items(name="Hagia Sophia", description="""Hagia Sophia was a
                     Greek Orthodox Christian patriarchal basilica (church),
                     later an imperial mosque, and now a museum
                     in Istanbul, Turkey.""",
                     category_id="1")
session.add(hagia_sophia)

kremlin = Items(name="Kremlin", description="""The Moscow Kremlin
                usually referred to as the
                Kremlin, is a fortified complex at the heart of Moscow,
                overlooking the Moskva River to the south, Saint Basil's
                Cathedral and Red Square to the east, and the Alexander
                Garden to the west.""",
                category_id="2")
session.add(kremlin)


palace = Items(name="Winterpalace of Petersburg", description="""The Winter
               Palace in
               Saint Petersburg, Russia, was, from 1732 to 1917, the official
               residence of the Russian monarchs. Today, the restored palace
               forms part of a complex of buildings housing the Hermitage
               Museum.""", category_id="4")
session.add(palace)

tower = Items(name="Tower of London", description="""he Tower of London, 
              officially Her
              Majesty's Royal Palace and Fortress of the Tower of London, is a
              historic castle located on the north bank of the River Thames in
              central London.""", category_id="3")
session.add(tower)

brandenburg_gate = Items(name="Brandenburger Tor",
                         description="""The Brandenburg Gate (German:
                             Brandenburger Tor) is an 18th-century neoclassical
                             monument in Berlin, built on the orders of
                             Prussian king Frederick William II after the
                             (temporarily) successful restoration of order
                             during the early Batavian Revolution.[1]""",
                         category_id="5")
session.add(brandenburg_gate)

plaza_mayor = Items(name="Plaza Mayor", description="""The Plaza Mayor
                    (English Main Square) was built during Philip III reign
                    and is a central plaza in the city of Madrid,
                    Spain. It is located only a few Spanish blocks away from
                    another famous plaza, the Puerta del Sol.""",
                    category_id="6")
session.add(plaza_mayor)

sophia_cathedrale = Items(name="Saint Sophias's Cathedral", description="""
                          Saint Sophia Cathedral in Kiev is an outstanding
                          architectural monument of Kievan Rus'. The cathedral
                          is one of the city's best known landmarks and the
                          first heritage site in Ukraine to be inscribed on
                          the World Heritage List along with the Kiev Cave
                          Monastery complex.""", category_id="7")
session.add(sophia_cathedrale)

colosseum = Items(name="Colosseum", description="""The Colosseum or Coliseum
                  
                  , also known as the Flavian Amphitheatre (Latin: 
                      Amphitheatrum Flavium; Italian:                      
                      Anfiteatro Flavio or Colosseo
                      , is an oval amphitheatre in the centre of
                      the city of Rome, Italy. Built of concrete and sand,[1]
                      it is the largest amphitheatre ever built.""",
                  category_id="8")
session.add(colosseum)

eiffel_tower = Items(name="Eiffel Tower", description="""The Eiffel Tower
                     is a
                     wrought iron lattice tower on the Champ de Mars in Paris,
                     France. It is named after the engineer Gustave Eiffel,
                     whose company designed and built the tower.""",
                     category_id="9")
session.add(eiffel_tower)

red_church = Items(name="Church of Simon and Helena", description="""Church of
                   Saints Simon and Helena also known as the Red Churchis a
                   Roman Catholic church on Independence Square in Minsk,
                   Belarus. This neo-Romanesque church was designed by Polish
                   architects Tomasz Pajzderski and Wladislaw Marconi.""",
                   category_id="10")
session.add(red_church)

# commiting all changes of both tables
session.commit()

# showing user the success of populating the database
print("DB populated")
