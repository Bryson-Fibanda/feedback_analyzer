import re
from collections import Counter
import random


class SentimentAnalyzer:
    def __init__(self):
        # Comprehensive sentiment word lists
        self.positive_words = {
            'good', 'great', 'excellent', 'amazing', 'love', 'awesome', 'fantastic',
            'perfect', 'best', 'recommend', 'happy', 'nice', 'wonderful', 'outstanding',
            'brilliant', 'superb', 'pleasant', 'satisfied', 'impressed', 'quick', 'fast',
            'easy', 'smooth', 'reliable', 'helpful', 'friendly', 'professional', 'quality',
            'exceeded', 'perfectly', 'seamless', 'efficient', 'responsive', 'outstanding',
            'pleased', 'delighted', 'terrific', 'marvelous', 'exceptional', 'stellar',
            'phenomenal', 'splendid', 'commendable', 'praiseworthy', 'admirable',
            'worth', 'valuable', 'beneficial', 'advantageous', 'enjoyable', 'pleasurable'
        }

        self.negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'hate', 'worst', 'poor', 'disappointed',
            'waste', 'rubbish', 'useless', 'broken', 'slow', 'disgusting', 'frustrating',
            'never', 'avoid', 'issue', 'problem', 'complaint', 'angry', 'furious',
            'annoying', 'frustrated', 'displeased', 'unsatisfied', 'unhappy', 'regret',
            'rubbish', 'garbage', 'trash', 'junk', 'scam', 'fraud', 'fake', 'defective',
            'faulty', 'damaged', 'expired', 'overpriced', 'expensive', 'costly', 'unfair',
            'unreliable', 'unprofessional', 'rude', 'ignored', 'neglected', 'abandoned',
            'useless', 'pointless', 'hopeless', 'miserable', 'dreadful', 'atrocious',
            'appalling', 'lousy', 'subpar', 'inferior', 'mediocre', 'unacceptable'
        }

        # Intensifiers that amplify sentiment
        self.intensifiers = {
            'very', 'really', 'extremely', 'absolutely', 'completely', 'totally',
            'utterly', 'highly', 'exceptionally', 'incredibly', 'remarkably'
        }

        # Negation words that flip sentiment
        self.negations = {'not', 'no', 'never', 'none', 'nothing', 'nowhere', 'neither', 'nor'}

    def analyze_sentiment(self, text):
        """Advanced sentiment analysis without external dependencies"""
        text_lower = text.lower()
        words = self._extract_words(text_lower)

        if not words:
            return 0.0

        positive_score = 0
        negative_score = 0
        negation_active = False
        intensity_multiplier = 1.0

        for i, word in enumerate(words):
            # Check for negations
            if word in self.negations:
                negation_active = True
                continue

            # Check for intensifiers
            if word in self.intensifiers:
                intensity_multiplier = 2.0
                continue

            # Check sentiment words
            if word in self.positive_words:
                score = 1.0 if not negation_active else -1.0
                positive_score += score * intensity_multiplier
                negation_active = False
                intensity_multiplier = 1.0

            elif word in self.negative_words:
                score = -1.0 if not negation_active else 1.0
                negative_score += score * intensity_multiplier
                negation_active = False
                intensity_multiplier = 1.0

        # Calculate final sentiment (-1 to 1 scale)
        total_score = positive_score + negative_score
        max_possible = len(words) * 2  # Theoretical maximum

        if max_possible == 0:
            return 0.0

        sentiment = total_score / max_possible
        return max(-1.0, min(1.0, sentiment))  # Clamp between -1 and 1

    def _extract_words(self, text):
        """Extract meaningful words from text"""
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        # Remove very common stop words
        stop_words = {
            'the', 'and', 'this', 'that', 'with', 'have', 'from', 'they', 'were', 'been',
            'what', 'when', 'where', 'which', 'their', 'would', 'should', 'could', 'about',
            'your', 'some', 'than', 'just', 'like', 'then', 'its', 'into', 'for', 'but',
            'not', 'are', 'was', 'had', 'has', 'will', 'all', 'you', 'there', 'been'
        }
        return [word for word in words if word not in stop_words]


# Global analyzer instance
analyzer = SentimentAnalyzer()


def analyze_feedback(reviews, analysis_type='basic'):
    """Analyze customer feedback and extract insights"""

    positive_reviews = []
    negative_reviews = []
    neutral_reviews = []

    # Analyze each review
    for review in reviews:
        sentiment = analyzer.analyze_sentiment(review)

        if sentiment > 0.1:
            positive_reviews.append({
                'text': review,
                'sentiment': sentiment,
                'keywords': extract_keywords(review),
                'analysis_method': 'advanced'
            })
        elif sentiment < -0.1:
            negative_reviews.append({
                'text': review,
                'sentiment': sentiment,
                'keywords': extract_keywords(review),
                'analysis_method': 'advanced'
            })
        else:
            neutral_reviews.append({
                'text': review,
                'sentiment': sentiment,
                'keywords': extract_keywords(review),
                'analysis_method': 'advanced'
            })

    # Extract common themes
    positive_themes = extract_common_themes(positive_reviews)
    negative_themes = extract_common_themes(negative_reviews)

    # Calculate percentages
    total = len(reviews)
    positive_pct = (len(positive_reviews) / total) * 100 if total > 0 else 0
    negative_pct = (len(negative_reviews) / total) * 100 if total > 0 else 0
    neutral_pct = (len(neutral_reviews) / total) * 100 if total > 0 else 0

    return {
        'summary': {
            'total_positive': len(positive_reviews),
            'total_negative': len(negative_reviews),
            'total_neutral': len(neutral_reviews),
            'positive_percentage': round(positive_pct, 1),
            'negative_percentage': round(negative_pct, 1),
            'neutral_percentage': round(neutral_pct, 1),
            'overall_sentiment': 'Positive' if positive_pct > negative_pct else 'Negative' if negative_pct > positive_pct else 'Neutral',
            'analysis_method': 'advanced_builtin'
        },
        'positive_reviews': positive_reviews[:10],
        'negative_reviews': negative_reviews[:10],
        'positive_themes': positive_themes,
        'negative_themes': negative_themes,
        'analysis_type': analysis_type
    }


def extract_keywords(text):
    """Extract important keywords from text"""
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())

    # Comprehensive stop words list
    stop_words = {
        'this', 'that', 'with', 'have', 'from', 'they', 'were', 'been', 'what',
        'when', 'where', 'which', 'their', 'would', 'should', 'could', 'about',
        'your', 'some', 'than', 'just', 'like', 'then', 'its', 'into', 'for',
        'but', 'not', 'are', 'was', 'had', 'has', 'will', 'all', 'you', 'there',
        'been', 'also', 'more', 'other', 'only', 'new', 'any', 'each', 'such',
        'how', 'many', 'most', 'even', 'much', 'both', 'being', 'because',
        'during', 'before', 'after', 'while', 'whereas', 'although', 'though',
        'since', 'until', 'unless', 'whether', 'while', 'once', 'however',
        'therefore', 'moreover', 'furthermore', 'nevertheless', 'nonetheless'
    }

    keywords = [word for word in words if word not in stop_words]

    # Count frequency and return most common
    word_counts = Counter(keywords)
    return [word for word, count in word_counts.most_common(5)]


def extract_common_themes(reviews):
    """Extract common themes from reviews"""
    all_keywords = []
    for review in reviews:
        all_keywords.extend(review['keywords'])

    keyword_counts = Counter(all_keywords)
    return keyword_counts.most_common(10)


def generate_response_suggestions(negative_reviews):
    """Generate AI-powered response suggestions for negative reviews"""
    suggestions = []

    response_templates = {
        'delivery': [
            "We sincerely apologize for the delivery delay. We're working with our logistics partner to ensure faster service in the future.",
            "Thank you for your patience. We understand the frustration with delayed delivery and are improving our shipping processes."
        ],
        'quality': [
            "We're sorry to hear the product didn't meet your expectations. We'd like to make this right - please contact support for a replacement.",
            "Thank you for the honest feedback about quality. We're reviewing this with our quality team to prevent future issues."
        ],
        'service': [
            "We apologize for the service experience. We're retraining our team to ensure better customer interactions.",
            "We're concerned about your service experience and would appreciate more details to help us improve."
        ],
        'price': [
            "We appreciate your feedback about pricing. We strive to balance quality with affordability and would love to discuss options.",
            "Thank you for sharing your thoughts on pricing. We regularly review our rates to ensure fair value."
        ],
        'general': [
            "We appreciate your honest feedback and take it seriously. We're committed to improving and would value the chance to make things right.",
            "Thank you for bringing this to our attention. We're always looking to improve and your feedback helps us grow."
        ]
    }

    for review in negative_reviews:
        text = review['text'] if isinstance(review, dict) else review
        text_lower = text.lower()

        # Determine the category
        if any(word in text_lower for word in ['slow', 'wait', 'time', 'late', 'delayed', 'delivery', 'shipping']):
            category = 'delivery'
        elif any(word in text_lower for word in
                 ['broken', 'not work', 'stopped', 'damage', 'defective', 'quality', 'poor']):
            category = 'quality'
        elif any(word in text_lower for word in ['rude', 'unprofessional', 'unhelpful', 'ignore', 'service', 'staff']):
            category = 'service'
        elif any(word in text_lower for word in ['expensive', 'price', 'cost', 'money', 'overpriced']):
            category = 'price'
        else:
            category = 'general'

        # Select random template from the category
        template = random.choice(response_templates[category])

        suggestions.append({
            'original_review': text,
            'suggested_response': template,
            'category': category
        })

    return suggestions