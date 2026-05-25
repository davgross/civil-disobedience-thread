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
