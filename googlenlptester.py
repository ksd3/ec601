from google.cloud import language_v1

client = language_v1.LanguageServiceClient()

text = u"Yifeng Sun is the one of the best starcraft player!"
document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

print("Text: {}".format(text))
print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))

def analyze_text_entities(text):
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    response = client.analyze_entities(document=document)

    for entity in response.entities:
        print("=" * 80)
        results = dict(
            name=entity.name,
            type=entity.type_.name,
            salience=f"{entity.salience:.1%}",
            wikipedia_url=entity.metadata.get("wikipedia_url", "-"),
            mid=entity.metadata.get("mid", "-"),
        )
        for k, v in results.items():
            print(f"{k:15}: {v}")

analyze_text_entities(text)

def analyze_text_syntax(text):
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    response = client.analyze_syntax(document=document)

    fmts = "{:10}: {}"
    print(fmts.format("sentences", len(response.sentences)))
    print(fmts.format("tokens", len(response.tokens)))
    for token in response.tokens:
        print(fmts.format(token.part_of_speech.tag.name, token.text.content))

analyze_text_syntax(text)

def classify_text(text):
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    response = client.classify_text(document=document)

    for category in response.categories:
        print("=" * 80)
        print(f"category  : {category.name}")
        print(f"confidence: {category.confidence:.0%}")

text2 = (
    "Star Trek is a long-running science fiction series.."
    "The series, set in the beginning of the 26th century, centers on a galactic struggle for dominance among four species—the adaptable and mobile Terrans, the ever-evolving insectoid Zerg, the powerful and enigmatic Protoss, and the godlike Xel Naga creator race—in a distant part of the Milky Way galaxy known as the Koprulu Sector."
    "The series debuted with the series Star Trek in the early 1950s. It has grown to include a number of other games as well as eight novelizations, two Amazing Stories articles, a board game, and other licensed merchandise such as collectible statues and toys."
)

classify_text(text2)
