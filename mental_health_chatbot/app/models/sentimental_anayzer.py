from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        self.history = []

    def analyze(self, text):
        scores = self.analyzer.polarity_scores(text)
        compound_score = scores['compound']
        self.history.append(compound_score)
        avg_score = self.calculate_average_score()
        return {
            'compound_score': compound_score,
            'average_score': avg_score
        }

    def calculate_average_score(self):
        recent_scores = self.history[-5:]
        if not recent_scores:
            return 0.0
        return sum(recent_scores) / len(recent_scores)