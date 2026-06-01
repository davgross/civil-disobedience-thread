#!/usr/bin/env python3
"""
Generate selfie-style AI portrait avatars via pollinations.ai (free, no API key).
Run:  python3 generate_avatars.py
Output goes to avatars/ subdirectory.
"""
import os, sys, time, urllib.request, urllib.parse

os.makedirs('avatars', exist_ok=True)

# Shared style suffix appended to every prompt
STYLE = (
    "close-up portrait photo, looking directly at camera, "
    "warm natural light, shallow depth of field, color photograph, "
    "photorealistic, high resolution, casual candid"
)

SUBJECTS = [
    ("thoreau", 1001,
     "Henry David Thoreau aged 32, 1849 New England, "
     "tousled brown hair, short scruffy beard, worn wool coat, "
     "intense earnest gaze, outdoors near a pond, " + STYLE),

    ("alcott", 1002,
     "Amos Bronson Alcott aged 50, 1849, American philosopher-educator, "
     "silver hair swept back, kind weathered face, "
     "dark frock coat and cravat, study bookshelf behind him, " + STYLE),

    ("emerson", 1003,
     "Ralph Waldo Emerson aged 46, 1849, American essayist, "
     "strong angular features, neatly combed dark hair going grey, "
     "formal black coat and white cravat, serene confident expression, " + STYLE),

    ("tolstoy", 1004,
     "Leo Tolstoy aged 40, 1869 Russia, novelist, "
     "full dark beard, deep-set intelligent eyes, "
     "simple Russian peasant shirt, windswept outdoor setting, " + STYLE),

    ("gandhi", 1005,
     "Mohandas Gandhi aged 55, 1924 India, "
     "clean-shaved head, wire-rimmed round spectacles, "
     "plain white cotton dhoti, warm gentle expression, "
     "sun-drenched outdoor light, " + STYLE),

    ("king", 1006,
     "Martin Luther King Jr aged 34, 1963 Atlanta, "
     "clean-cut young Black man, confident dignified expression, "
     "dark suit white shirt dark tie, "
     "warm indoor light, " + STYLE),

    ("arendt", 1007,
     "Hannah Arendt aged 57, 1963 New York City, "
     "intellectual German-American woman, dark wavy hair, "
     "holding a cigarette, serious but open expression, "
     "1960s-style dark turtleneck, city window behind her, " + STYLE),

    ("debs", 1008,
     "Eugene V. Debs aged 55, 1910 Indiana, labor organizer, "
     "bald head, clean-shaven, strong jaw, "
     "earnest working-class expression, "
     "plain collar shirt and suspenders, " + STYLE),

    ("senatorwebster", 1009,
     "Daniel Webster aged 45, 1827 New England, United States Senator, "
     "imposing American statesman, striking dark eyes with heavy brows, "
     "strong jaw, dark hair swept back from broad forehead, "
     "formal black coat and white cravat, patrician confident bearing, " + STYLE),

    ("redemma", 1020,
     "Emma Goldman aged 35, 1904, Russian-American anarchist, "
     "dark hair pinned up, round wire-rimmed glasses, "
     "strong-featured woman with confident direct gaze, "
     "high-collared blouse, indoor setting, " + STYLE),

    ("amalcott", 1021,
     "Abby May Alcott aged 45, 1845 Concord Massachusetts, social reformer and diarist, "
     "determined kind face, dark hair neatly parted and pinned, "
     "plain dark Victorian dress with white collar, "
     "warm compassionate expression, simple domestic interior, " + STYLE),

    ("hgoblake", 1022,
     "Harrison Gray Otis Blake aged 38, 1854 Worcester Massachusetts, schoolmaster, "
     "serious thoughtful young man, dark hair, clean-shaven, "
     "plain frock coat and white collar, "
     "earnest devoted expression, modest study interior, " + STYLE),

    ("hennacy", 1023,
     "Ammon Hennacy aged 50, 1943, American Catholic Worker pacifist and tax resister, "
     "lean angular face, close-cropped graying hair, clean-shaven, "
     "plain working-man's shirt, direct defiant gaze, "
     "outdoor urban setting, " + STYLE),

    ("MartinBuber", 1024,
     "Martin Buber aged 60, 1938, Austrian-born Jewish philosopher and theologian, "
     "full white beard, deep-set wise eyes behind round spectacles, "
     "high forehead, thoughtful open expression, "
     "dark suit and tie, simple study with books, " + STYLE),

    ("TheodoreBaird", 1025,
     "Theodore Baird aged 55, 1956, American English professor at Amherst College, "
     "lean Yankee face, graying hair, wire-rimmed spectacles, "
     "dry skeptical expression, tweed jacket and tie, "
     "academic office lined with books, " + STYLE),

    ("WillardUphaus", 1026,
     "Willard Uphaus aged 65, 1955, American Christian pacifist, "
     "kind earnest face, silver hair, clean-shaven, "
     "plain white collar shirt, warm direct gaze, "
     "outdoor New England setting near a lodge, " + STYLE),

    ("leo-stoller", 1027,
     "Leo Stoller aged 45, 1957, American writer and Thoreau devotee, "
     "rumpled intellectual, dark hair going gray, "
     "open-collar shirt, earnest argumentative expression, "
     "cluttered urban study, " + STYLE),

    ("PaulLauter", 1028,
     "Paul Lauter aged 30, 1962, American literary critic and activist, "
     "young earnest man, dark hair, clean-shaven, "
     "open-collar button-down shirt, engaged direct gaze, "
     "civil rights era setting, " + STYLE),

    ("RevEzraRipley", 1029,
     "Reverend Ezra Ripley aged 70, 1821 Concord Massachusetts, Puritan Congregationalist minister, "
     "severe patriarchal face, white powdered hair, "
     "black clerical coat and white bands, "
     "plain New England church interior, dignified unyielding expression, " + STYLE),

    ("william_stuart_nelson", 1030,
     "William Stuart Nelson aged 55, 1950, African American educator and Gandhian scholar, "
     "dignified scholarly man, close-cropped gray-black hair, "
     "dark suit and tie, calm authoritative expression, "
     "university office with books, warm indoor light, " + STYLE),

    ("JohnBurroughs", 1032,
     "John Burroughs aged 55, 1892, American naturalist and nature essayist, "
     "full white beard, deep-set observant eyes, weathered outdoor face, "
     "plain dark coat, seated outdoors among trees, Hudson Valley, "
     "relaxed genial expression, " + STYLE),

    ("s-a-jones", 1033,
     "Samuel Arthur Jones aged 50, 1884, Victorian American physician and scholar, "
     "dark beard streaked with gray, wire-rimmed spectacles, "
     "formal dark suit and high collar, earnest devoted expression, "
     "study with books and papers, " + STYLE),

    ("h-a-page", 1034,
     "Alexander Hay Japp aged 40, 1877 Edinburgh Scotland, Scottish Victorian author and editor, "
     "dark mutton-chop sideburns, serious literary expression, "
     "dark Victorian frock coat and cravat, "
     "book-lined study, " + STYLE),

    ("RichardDrinnon", 1035,
     "Richard Drinnon aged 40, 1965, American historian and anarchist scholar, "
     "lean intellectual face, dark hair, clean-shaven, "
     "open-collar shirt, direct thoughtful gaze, "
     "study with books, 1960s setting, " + STYLE),

    ("HerbertFaulknerWest", 1055,
     "Herbert Faulkner West aged 50, 1948, American literary critic and Dartmouth professor, "
     "thoughtful patrician face, graying hair, wire-rimmed glasses, "
     "tweed jacket and tie, measured earnest expression, "
     "faculty office with books, " + STYLE),

    ("richardgroff", 1056,
     "Richard Groff aged 45, 1961 Pennsylvania, American war tax resister and writer, "
     "plain principled face, close-cropped graying hair, clean-shaven, "
     "plain working shirt, quiet determined expression, "
     "simple domestic interior, " + STYLE),

    ("sophiadobsoncollet", 1048,
     "Sophia Dobson Collet aged 35, 1857 London England, English radical journalist and freethinker, "
     "dark hair neatly parted, plain Victorian dress, "
     "earnest intellectual expression, "
     "simple study with books and papers, " + STYLE),

    ("RevJamesRobinson", 1049,
     "Reverend James Herman Robinson aged 45, 1952 New York City, African American minister and civil rights leader, "
     "dignified man, short hair, clean-shaven, "
     "clerical collar and dark jacket, warm determined expression, "
     "church interior, " + STYLE),

    ("williamrobertmiller", 1050,
     "William Robert Miller aged 35, 1962, American pacifist writer and editor, "
     "earnest young man, dark hair, clean-shaven, "
     "plain open-collar shirt, thoughtful principled expression, "
     "modest study, " + STYLE),

    ("JohnHarlandHicks", 1051,
     "John H. Hicks aged 45, 1966, American literary scholar and professor, "
     "mild academic face, graying hair, wire-rimmed glasses, "
     "tweed jacket, careful analytical expression, "
     "university office with books, " + STYLE),

    ("georgewoodcock", 1052,
     "George Woodcock aged 50, 1962 Vancouver Canada, Canadian anarchist writer and literary critic, "
     "lean face, dark hair going gray, thoughtful intense eyes, "
     "plain dark jacket, "
     "study with books and manuscripts, " + STYLE),

    ("samstaples", 1053,
     "Sam Staples aged 40, 1855 Concord Massachusetts, New England town constable, "
     "plain sturdy Yankee face, clean-shaven, "
     "practical working-man's coat and hat, "
     "direct no-nonsense expression, village street or store interior, " + STYLE),

    ("nicholaswalter", 1054,
     "Nicholas Walter aged 35, 1969 London England, British anarchist journalist and writer, "
     "lean young man, dark hair, earnest principled expression, "
     "plain open-collar shirt, "
     "urban London setting, " + STYLE),

    ("aestheticpeabody", 1041,
     "Elizabeth Palmer Peabody aged 45, 1849 Boston Massachusetts, American educator and transcendentalist publisher, "
     "dark hair parted in the middle, earnest open face, "
     "plain dark Victorian dress with white collar, "
     "warm intelligent expression, bookshop interior, " + STYLE),

    ("benjamintucker", 1042,
     "Benjamin Tucker aged 35, 1889 Boston Massachusetts, American individualist anarchist and editor, "
     "dark hair and full beard, sharp determined eyes, "
     "plain dark suit, direct uncompromising gaze, "
     "study with papers and books, " + STYLE),

    ("sagitta", 1043,
     "John Henry Mackay aged 35, 1899 Berlin Germany, Scottish-born German individualist anarchist and writer, "
     "dark wavy hair, neat mustache, intense literary expression, "
     "dark late-Victorian suit and cravat, "
     "urban study interior, " + STYLE),

    ("twparsons", 1044,
     "Thomas William Parsons aged 35, 1854 Boston Massachusetts, American poet and dentist, "
     "dark hair, clean-shaven, thoughtful skeptical expression, "
     "plain dark frock coat and white collar, "
     "modest Victorian study, " + STYLE),

    ("WalterHarding", 1045,
     "Walter Harding aged 45, 1962, American scholar and professor, "
     "mild-mannered academic, dark hair going gray, wire-rimmed glasses, "
     "tweed jacket, warm earnest expression, "
     "university office lined with books, " + STYLE),

    ("linyutang", 1046,
     "Lin Yutang aged 45, 1940 New York City, Chinese-American writer and philosopher, "
     "distinguished Chinese man, dark hair, round tortoiseshell glasses, "
     "gentle humorous expression, dark suit, "
     "comfortable study with East-meets-West decor, warm light, " + STYLE),

    ("rudolfrocker", 1047,
     "Rudolf Rocker aged 50, 1923, German anarcho-syndicalist organizer and writer, "
     "strong face, full dark beard streaked with gray, "
     "plain working-class jacket, earnest resolute expression, "
     "simple indoor setting, " + STYLE),

    ("JSMill", 1039,
     "John Stuart Mill aged 45, 1851 London England, British philosopher and political economist, "
     "high forehead, receding dark hair, clean-shaven, "
     "dark Victorian frock coat and white cravat, "
     "serious intellectual expression, study with books, " + STYLE),

    ("deTocqueville", 1040,
     "Alexis de Tocqueville aged 30, 1835 Paris France, French aristocrat and political thinker, "
     "slender refined face, dark wavy hair, clean-shaven, "
     "aristocratic bearing, dark coat and white cravat, "
     "thoughtful observant expression, elegant study, " + STYLE),

    ("leon-bazalgette", 1036,
     "Léon Bazalgette aged 40, 1913 Paris France, French literary critic and translator, "
     "dark mustache, dark wavy hair, pince-nez spectacles, "
     "dark suit and cravat, thoughtful literary expression, "
     "Parisian study with books, warm lamplight, " + STYLE),

    ("TheNewYorker", 1037,
     "Eustace Tilley, Art Deco dandy, 1925 New York City, "
     "top hat, high Regency collar, holds a monocle up to one eye examining a butterfly, "
     "languid aristocratic expression of supreme detachment, "
     "pen-and-ink illustration style portrait, white background, "
     "close-up portrait, looking directly at viewer, high contrast, elegant line art"),

    ("TrumanJNelson", 1038,
     "Truman Nelson aged 50, 1961, American radical novelist and historian, "
     "lean weathered working-class face, dark hair graying at temples, clean-shaven, "
     "plain open-collar shirt, serious combative expression, "
     "New England coastal setting, " + STYLE),

    ("trevor-nw-bush", 1031,
     "Trevor Bush aged 55, 1965 Johannesburg South Africa, white South African Anglican priest and anti-apartheid activist, "
     "lean weathered face, steel-gray hair, clean-shaven, "
     "clerical collar and dark jacket, grave resolute expression, "
     "simple church interior, " + STYLE),

    ("tusitala", 1018,
     "Robert Louis Stevenson aged 35, 1885, Scottish novelist, "
     "slender man, long wavy dark hair, thin mustache, dark intense eyes, "
     "Victorian cravat and dark velvet jacket, romantic adventurous expression, "
     "warm candlelit study with books, " + STYLE),

    ("JamesMacKaye", 1019,
     "James MacKaye aged 55, 1927, American philosopher, "
     "scholarly man with round wire-rimmed spectacles, dark graying hair, "
     "formal suit and tie, thoughtful analytical expression, "
     "academic office with bookshelves, " + STYLE),

    ("anonym", 1017,
     "Danish resistance member aged 55, 1977, Northern European man, "
     "gray-streaked hair, weathered thoughtful face, plain wool jacket, "
     "serious dignified expression, simple indoor setting, " + STYLE),

    ("george_peele", 1015,
     "George Peele aged 30, 1586 London, Elizabethan playwright and poet, "
     "dark hair, period doublet and ruff collar, animated expressive face, "
     "candlelit tavern setting, lively literary air, " + STYLE),

    ("larosenwa", 1016,
     "Larry Rosenwald aged 71, 2018, American English professor, "
     "white-haired man with short gray-white hair, round tortoiseshell glasses, "
     "light complexion, blue open-collar shirt under gray-brown tweed sport jacket, "
     "friendly thoughtful expression looking slightly to the side, "
     "office with bookshelves behind him, warm indoor light, " + STYLE),

    ("kongqiu", 1014,
     "Confucius aged 60, 500 BCE China, Chinese philosopher and teacher, "
     "elder man with long white beard, traditional Han dynasty scholar's robes and cap, "
     "serene dignified expression, warm diffuse light, simple scholarly study, " + STYLE),

    ("thomas_middleton", 1012,
     "Thomas Middleton aged 40, 1620 London, Jacobean playwright, "
     "dark hair, Jacobean ruff collar, period doublet, quill pen nearby, "
     "candlelit study with manuscripts, sardonic intelligent expression, " + STYLE),

    ("williampaley", 1013,
     "William Paley aged 55, 1798 northern England, Anglican clergyman and philosopher, "
     "powdered white wig, clerical collar and dark robes, round genial face, "
     "study with leather-bound books, Enlightenment era, " + STYLE),

    ("thebard", 1011,
     "William Shakespeare aged 45, 1609 London, Elizabethan playwright and poet, "
     "balding with remaining brown hair, small neat mustache and pointed beard, "
     "white Elizabethan ruff collar, dark doublet, thoughtful intelligent expression, "
     "warm candlelight, " + STYLE),

    ("charleswolfe", 1010,
     "Charles Wolfe aged 25, 1816 Ireland, Irish curate and poet, "
     "pale thoughtful young man, dark hair, clerical collar and coat, "
     "gentle melancholy expression, soft diffuse overcast light, " + STYLE),

    ("brahkumarnehru", 1057,
     "B.K. Nehru aged 50, 1960 Washington DC, Indian diplomat and Ambassador to United States, "
     "distinguished South Asian man, dark short hair, clean-shaven, "
     "formal suit and tie, composed authoritative expression, "
     "diplomatic office setting, warm indoor light, " + STYLE),

    ("brooksatkinson", 1058,
     "Brooks Atkinson aged 55, 1949 New York City, American theater critic and naturalist, "
     "lean thoughtful man, round wire-rimmed glasses, dark suit, "
     "slightly serious reflective expression, "
     "theater or study background, " + STYLE),

    ("brucewatson", 1059,
     "Bruce Watson aged 35, 1965 United States, American journalist and civil rights commentator, "
     "earnest face, dark hair, plain mid-century suit, "
     "engaged determined expression, "
     "simple office setting, " + STYLE),

    ("carrollhollis", 1060,
     "Carroll Hollis aged 45, 1949 United States, American literary scholar and Thoreau specialist, "
     "academic man, glasses, conservative suit, "
     "thoughtful bookish expression, "
     "university office with books, " + STYLE),

    ("charlesmadison", 1061,
     "Charles A. Madison aged 50, 1947 United States, American literary historian and editor, "
     "older man with round face, wire-rimmed glasses, conservative suit, "
     "warm thoughtful expression, "
     "book-lined study, " + STYLE),

    ("edwarddahlberg", 1062,
     "Edward Dahlberg aged 45, 1945 New York, American novelist and essayist, "
     "gaunt angular face, intense dark eyes, dark hair slicked back, "
     "open-collar shirt, uncompromising fierce expression, "
     "sparse literary apartment, harsh light, " + STYLE),

    ("garrywills", 1063,
     "Garry Wills aged 40, 1975 United States, American journalist and historian, "
     "lean man with dark hair, wire-rimmed glasses, "
     "casual academic jacket, incisive intelligent expression, "
     "study with books and papers, " + STYLE),

    ("GilbertSeldes", 1064,
     "Gilbert Seldes aged 40, 1933 New York City, American journalist and cultural critic, "
     "sharp-featured man, dark hair, suit with pocket square, "
     "sardonic worldly expression, "
     "urban New York setting, " + STYLE),

    ("HarryVJaffa", 1065,
     "Harry V. Jaffa aged 55, 1973 Claremont California, American political philosopher, "
     "round earnest face, gray hair, thick-framed glasses, "
     "dark academic suit, serious intense expression, "
     "academic office with American historical books, " + STYLE),

    ("heinzeulau", 1066,
     "Heinz Eulau aged 45, 1960 Stanford California, American political scientist, "
     "lean intelligent face, gray-tinged dark hair, wire-rimmed glasses, "
     "academic tweed jacket, analytical expression, "
     "university office setting, " + STYLE),

    ("HenryMiller", 1067,
     "Henry Miller aged 55, 1946 Big Sur California, American novelist, "
     "tanned bald head, bright knowing eyes, open-collar shirt, "
     "relaxed earthy expression with slight irreverence, "
     "California coastal setting, natural light, " + STYLE),

    ("HerbertJStoring", 1068,
     "Herbert J. Storing aged 40, 1968 Chicago, American political scientist, "
     "dark-haired scholarly man, clean-shaven, dark-framed glasses, "
     "trim suit, serious engaged expression, "
     "University of Chicago office, " + STYLE),

    ("hugobedau", 1069,
     "Hugo Adam Bedau aged 45, 1971 Boston Massachusetts, American philosopher, "
     "trim professorial man, short dark hair, wire-rimmed glasses, "
     "academic jacket, thoughtful principled expression, "
     "Tufts University office with philosophy books, " + STYLE),

    ("JohnAlbertMacy", 1070,
     "John Albert Macy aged 35, 1913 New York City, American literary critic and socialist, "
     "lean thoughtful man, dark hair and mustache, period suit, "
     "earnest intellectual expression, "
     "study with books and periodicals, " + STYLE),

    ("mariosavio", 1071,
     "Mario Savio aged 22, 1964 Berkeley California, American student activist and Free Speech Movement leader, "
     "young intense man, dark curly hair, open-collar shirt and jacket, "
     "passionate impassioned expression, mouth open in speech, "
     "Berkeley campus steps, outdoor light, " + STYLE),

    ("odellshepard", 1072,
     "Odell Shepard aged 55, 1939 Connecticut, American author and Lieutenant Governor, "
     "distinguished man, gray hair, clean-shaven, "
     "formal suit, cultured genial expression, "
     "New England study or statehouse interior, " + STYLE),

    ("richardboardman", 1073,
     "Richard Boardman aged 45, 1967 United States, American pacifist writer, "
     "plain sincere face, short dark hair, "
     "plain shirt or jacket, quiet reflective expression, "
     "simple domestic or meeting-house interior, " + STYLE),

    ("StanleyEdgarHyman", 1074,
     "Stanley Edgar Hyman aged 40, 1959 New York, American literary critic and New Yorker staff writer, "
     "round face with short dark hair and beard, thick glasses, "
     "rumpled academic jacket, witty sharp expression, "
     "cluttered study with stacked books, " + STYLE),

    ("vernonlouisparrington", 1075,
     "Vernon Louis Parrington aged 55, 1926 Seattle Washington, American historian and literary critic, "
     "lean distinguished man, gray hair, wire-rimmed glasses, "
     "dark academic suit, serious contemplative expression, "
     "University of Washington study with American history books, " + STYLE),

    ("AbeFortas", 1076,
     "Abe Fortas aged 58, 1968 Washington DC, Associate Justice of the United States Supreme Court, "
     "trim authoritative man, dark graying hair, clean-shaven, "
     "judicial robes or dark suit, composed confident expression, "
     "Supreme Court chamber, formal setting, " + STYLE),

    ("AlfredKazin", 1077,
     "Alfred Kazin aged 45, 1960 New York City, American literary critic and essayist, "
     "lean intense man, dark hair, wire-rimmed glasses, "
     "dark turtleneck or academic jacket, sharp intellectual expression, "
     "book-lined New York study, " + STYLE),

    ("BostonCourier", 1078,
     "Boston Courier newspaper office 1849, historic New England press room, "
     "large wooden printing press with type cases, stacks of broadsheets, "
     "inkstained workers in period aprons, gas lamps, "
     "busy nineteenth-century newspaper composing room, detailed period scene, " + STYLE),

    ("DonaldKaufman", 1079,
     "Donald D. Kaufman aged 40, 1973 Newton Kansas, American Mennonite pastor and peace advocate, "
     "earnest plain-featured man, short dark hair, clean-shaven, "
     "simple dark suit or minister's collar, quiet principled expression, "
     "modest church office or plain interior, soft light, " + STYLE),

    ("GregorySJay", 1080,
     "Gregory Jay aged 38, 1990 Milwaukee Wisconsin, American literary scholar and cultural critic, "
     "dark-haired professorial man, glasses, "
     "casual academic jacket, engaged critical expression, "
     "university office, " + STYLE),

    ("JohnBrown", 1081,
     "John Brown aged 58, 1858 Kansas, American abolitionist, "
     "gaunt intense old man with long white beard, deep-set burning eyes, "
     "plain dark coat, fierce prophetic expression, "
     "dramatic chiaroscuro lighting, stark background, " + STYLE),

    ("RaymondAdams", 1082,
     "Raymond Adams aged 45, 1944 United States, American literary scholar, "
     "earnest academic man, short dark hair, "
     "conservative suit, thoughtful careful expression, "
     "university library setting, " + STYLE),

    ("sadi", 1083,
     "Saadi Shirazi aged 60, 1258 Shiraz Persia, Persian Sufi poet, "
     "elder Persian man with white beard and mustache, "
     "white turban and flowing robes, serene wise expression, "
     "Persian garden or courtyard with tiles and roses, soft warm light, " + STYLE),

    ("TaylorStoehr", 1084,
     "Taylor Stoehr aged 48, 1979 United States, American literary scholar, "
     "trim intellectual man, short gray-streaked hair, "
     "academic jacket, reflective analytical expression, "
     "study with Thoreau and Emerson books, " + STYLE),

    ("WendellGlick", 1085,
     "Wendell Glick aged 36, 1952 United States, American literary scholar and Thoreau editor, "
     "earnest academic man, short dark hair, "
     "conservative suit, careful scholarly expression, "
     "library with manuscript papers and Thoreau texts, " + STYLE),

    ("WilliamJWolf", 1086,
     "William J. Wolf aged 55, 1973 United States, American Episcopal priest and theologian, "
     "distinguished man with graying temples, clerical collar or dark suit, "
     "warm serious expression, "
     "church office with theological books, " + STYLE),

    ("AJMuste", 1087,
     "A.J. Muste aged 60, 1945 New York City, American pacifist and labor organizer, "
     "lean earnest man, wire-rimmed glasses, thinning gray hair, "
     "plain dark suit or minister's collar, serious principled expression, "
     "union hall or peace organization office, " + STYLE),

    ("BarbaraDeming", 1088,
     "Barbara Deming aged 45, 1962 United States, American feminist writer and pacifist activist, "
     "strong-featured woman, short hair, plain blouse or jacket, "
     "calm determined expression, steady direct gaze, "
     "simple domestic or outdoor setting, natural light, " + STYLE),

    ("BobPeppermanTaylor", 1089,
     "Bob Pepperman Taylor aged 40, 1996 Burlington Vermont, American political theorist and professor, "
     "earnest professorial man, short dark hair, wire-rimmed glasses, "
     "academic jacket, thoughtful engaged expression, "
     "university office with political theory books, " + STYLE),

    ("BostonDailyTraveller", 1090,
     "Boston Daily Traveller newspaper office 1849, historic New England press room, "
     "wooden printing press with type cases, broadsheets on composing table, "
     "period workers in aprons, gas lamps casting warm light, "
     "busy nineteenth-century newspaper composing room, " + STYLE),

    ("BryanCaplan", 1091,
     "Bryan Caplan aged 35, 2006 Fairfax Virginia, American economist and libertarian blogger, "
     "boyish intellectual face, dark hair, wire-rimmed glasses, "
     "casual dress shirt, skeptical ironic expression, "
     "George Mason University office with economics books, " + STYLE),

    ("DailyChronotype", 1092,
     "Daily Chronotype newspaper office 1849, small Wisconsin Free Soil press room, "
     "hand-operated press with type cases, abolitionist broadsheets, "
     "two period compositors in aprons, simple frontier newspaper office, "
     "midwest pioneer interior, natural light from window, " + STYLE),

    ("DavidWelshRamparts", 1093,
     "David Welsh aged 28, 1966 San Francisco California, American New Left journalist and editor, "
     "young earnest man, dark hair, open-collar shirt, "
     "engaged activist expression, "
     "Ramparts magazine office with protest posters, " + STYLE),

    ("FBSanborn", 1094,
     "Franklin Benjamin Sanborn aged 50, 1882 Concord Massachusetts, American journalist and abolitionist, "
     "lean sharp-featured man with beard and mustache, dark eyes, "
     "period dark suit, intense earnest expression, "
     "Concord Massachusetts study with books and manuscripts, " + STYLE),

    ("JohnDear", 1095,
     "John Dear aged 40, 1999 United States, American Jesuit priest and peace activist, "
     "thin serious face, dark hair, clerical collar, "
     "quiet compassionate expression, "
     "simple church office or outdoor peace vigil, soft light, " + STYLE),

    ("KennettLove", 1096,
     "Kennett Love aged 38, 1962 New York City, American foreign correspondent and journalist, "
     "lean weathered face, short dark hair, correspondent's jacket, "
     "alert observant expression, "
     "newspaper office or foreign bureau setting, " + STYLE),

    ("NicholasMurrayButler", 1097,
     "Nicholas Murray Butler aged 62, 1924 New York City, American university president and Nobel laureate, "
     "portly distinguished man, gray hair, clean-shaven, "
     "dark formal suit with watch chain, authoritative self-assured expression, "
     "Columbia University presidential office, formal setting, " + STYLE),

    ("NormanThomas", 1098,
     "Norman Thomas aged 60, 1944 New York City, American socialist leader and presidential candidate, "
     "tall lean man, gray hair, clean-shaven, dark suit, "
     "earnest principled expression, "
     "campaign or meeting hall setting, " + STYLE),

    ("SusanSontag", 1099,
     "Susan Sontag aged 40, 1973 New York City, American essayist and cultural critic, "
     "striking woman with dark hair streaked with white, strong features, "
     "dark turtleneck, intense intellectual expression, "
     "book-lined New York apartment, warm light, " + STYLE),

    ("VictorHBalke", 1100,
     "Victor H. Balke aged 45, 1965 United States, American scholar and civil disobedience commentator, "
     "earnest academic man, short dark hair, wire-rimmed glasses, "
     "conservative suit, careful analytical expression, "
     "university office setting, " + STYLE),

    ("WaltWhitman", 1101,
     "Walt Whitman aged 50, 1869 Washington DC, American poet and journalist, "
     "full flowing white beard, broad-brimmed felt hat, open-collar shirt, "
     "expansive warm expression, relaxed democratic bearing, "
     "outdoor urban or pastoral setting, dappled light, " + STYLE),

    ("EricSevareid", 1102,
     "Eric Sevareid aged 55, 1967 Washington DC, American CBS News television correspondent and commentator, "
     "distinguished man with silver-gray hair, clean-shaven, serious broadcast-ready expression, "
     "dark suit and tie, television studio or press room background, "
     "professional composed demeanor, warm studio light, " + STYLE),

    ("TheNewEnglander", 1103,
     "The New Englander journal 1849, Victorian theological quarterly from New Haven Connecticut, "
     "leather-bound volume with gold-stamped cover on a reading desk, "
     "Puritan austerity, dark green binding, brass candlestick holder beside it, "
     "New England study interior, warm candlelight, engraving style"),

    ("SCOTUS", 1104,
     "United States Supreme Court chamber 1857, Washington DC, "
     "red velvet curtains, American eagle seal, nine empty mahogany chairs, "
     "white marble columns, solemnly lit formal chamber, "
     "period engraving aesthetic, dramatic chiaroscuro lighting"),

    ("TerenceBall", 1105,
     "Terence Ball aged 35, 1979 American academic, political theorist, "
     "thoughtful professorial man with dark hair, slight smile, "
     "book-lined office background, tweed or corduroy jacket, "
     "scholarly composed demeanor, warm office light, " + STYLE),

    ("JamesFChildress", 1106,
     "James F. Childress aged 35, 1975 American moral philosopher and ethicist, "
     "serious thoughtful man with brown hair and glasses, "
     "University of Virginia faculty office background, dark jacket, "
     "careful attentive expression, warm academic light, " + STYLE),

    ("CurtisCrawford", 1107,
     "Curtis Crawford aged 40, 1969 American political philosopher, "
     "earnest scholarly man in late middle age, dark hair, "
     "study or library background, conservative suit, "
     "analytical composed expression, warm office light, " + STYLE),

    ("NormanJacobson", 1108,
     "Norman Jacobson aged 45, 1969 UC Berkeley political theorist, "
     "intellectual American professor with salt-and-pepper hair, "
     "Berkeley campus office background, rumpled tweed jacket, "
     "warm searching expression, natural light through window, " + STYLE),

    ("HowardZinn", 1109,
     "Howard Zinn aged 45, 1967 American historian and activist, "
     "dark-haired energetic man with intense eyes and slight smile, "
     "Boston University campus or protest backdrop, open-collar shirt, "
     "passionate principled expression, natural daylight, " + STYLE),

    ("StaughtonLynd", 1110,
     "Staughton Lynd aged 37, 1966 American historian and civil rights activist, "
     "lean earnest man with dark-rimmed glasses and dark hair, "
     "study or protest meeting backdrop, plain jacket, "
     "serious committed expression, warm indoor light, " + STYLE),

    ("VaclavHavel", 1111,
     "Václav Havel aged 42, 1978 Czech playwright and dissident, "
     "pale blue-eyed man with sandy hair and mustache, "
     "Prague apartment or theater backdrop, turtleneck sweater, "
     "quietly determined expression, soft ambient light, " + STYLE),
]

BASE = "https://image.pollinations.ai/prompt/"

for name, seed, prompt in SUBJECTS:
    out = f"avatars/{name}.jpg"
    if os.path.exists(out) and os.path.getsize(out) > 5000:
        print(f"  {name}: already exists, skipping")
        continue

    encoded = urllib.parse.quote(prompt)
    url = f"{BASE}{encoded}?width=512&height=512&seed={seed}&model=flux&nologo=true"

    print(f"  {name}: generating…", flush=True)
    t0 = time.time()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
        with open(out, 'wb') as f:
            f.write(data)
        elapsed = time.time() - t0
        print(f"  {name}: saved {len(data)//1024} KB in {elapsed:.0f}s", flush=True)
    except Exception as e:
        print(f"  {name}: ERROR — {e}", file=sys.stderr)

    time.sleep(1)

print("Done. Check avatars/ directory.")
