import random
import hashlib # for seed generation
class SessionState: # Session state for seeded randomization
    def __init__(self):
        self.choices = []  # Track all user choices
        self.seed = 0
        self.rng = random.Random()
        self.log = []  # Log of choices and seeds
    def add_choice(self, choice_text, question_text): # Record a choice and update the seed
        self.choices.append(choice_text) # Create deterministic seed from all choices
        choice_string = "".join(self.choices)
        self.seed = int(hashlib.md5(choice_string.encode()).hexdigest()[:8], 16)
        self.rng.seed(self.seed)
        self.log.append(f"Choice: {choice_text} | Seed: {self.seed}")
    def get_seeded_choice(self, options): # Get a reproducible random choice based on current seed
        return self.rng.choice(options)
    def print_summary(self):
        from motors import get_position, get_offset_from_home, get_calibration
        pos = get_position()
        offset = get_offset_from_home()
        cal = get_calibration()
        print("\n  Session Summary:")
        print(f"  Choices made: {len(self.choices)}")
        print(f"  Freedom chosen: {self.choices.count('freedom')} times")
        if cal["calibrated"]:
            print(f"  Calibration (steps/revolution):")
            print(f"    Inner wheel: {cal['inner']}")
            print(f"    Outer wheel: {cal['outer']}")
        print(f"  Final wheel positions (steps from home):")
        print(f"    Inner: {pos['inner']:+d}")
        print(f"    Outer: {pos['outer']:+d}")
        print(f"    Total offset: {offset}")
        print(f"  Aligned: {'Yes' if offset <= 10 else 'No'}")
session = SessionState()
DISTRACTIONS = ["Money", "Wealth", "Possessions", "Luxury", "Property", "Riches", "Fortune", "Assets", "Inheritance", "Treasure", "Status", "Fame", "Recognition", "Popularity", "Reputation", "Prestige", "Influence", "Admiration", "Respect", "Attention", "Celebrity", "Notoriety", "Renown", "Glory", "Honor", "Distinction", "Prominence", "Clout", "Standing", "Rank", "Power", "Control", "Dominance", "Authority", "Command", "Leadership", "Supremacy", "Reign", "Mastery", "Leverage", "Approval", "Validation", "Acceptance", "Praise", "Compliments", "Flattery", "Adoration", "Worship", "Applause", "Endorsement", "Comfort", "Security", "Safety", "Stability", "Predictability", "Routine", "Familiarity", "Convenience", "Ease", "Shelter", "Success", "Achievement", "Accomplishment", "Victory", "Winning", "Triumph", "Conquest", "Excellence", "Greatness", "Legacy", "Perfection", "Certainty", "Answers", "Solutions", "Clarity", "Order", "Structure", "Plans", "Guarantees", "Assurance", "Pleasure", "Entertainment", "Distraction", "Escape", "Numbness", "Intoxication", "Indulgence", "Gratification", "Thrill", "Stimulation", "Pride", "Ego", "Self-importance", "Superiority", "Being right", "Arrogance", "Vanity", "Conceit", "Self-image", "Reputation", "Love from others", "Belonging", "Companionship", "Being needed", "Being wanted", "Devotion", "Loyalty", "Attachment", "Romance", "Intimacy", "Busyness", "Productivity", "Efficiency", "More time", "Speed", "Multitasking", "Hustle", "Grind", "Output", "Results", "Knowledge", "Understanding", "Wisdom", "Intelligence", "Expertise", "Credentials", "Degrees", "Titles", "Qualifications", "Genius", "Beauty", "Youth", "Health", "Strength", "Attractiveness", "Fitness", "Appearance", "Physique", "Looks", "Charm", "Happiness", "Joy", "Excitement", "Passion", "Meaning", "Purpose", "Fulfillment", "Contentment", "Bliss", "Euphoria", "Revenge", "Justice", "Fairness", "Being understood", "Being heard", "Being seen", "Mattering", "Significance", "Importance", "Relevance", "Independence", "Self-sufficiency", "Autonomy", "Solitude", "Privacy", "Boundaries", "Space", "Distance", "Detachment", "Isolation", "Connection", "Community", "Friendship", "Family", "Roots", "Tradition", "Heritage", "Identity", "Culture", "Tribe", "Adventure", "Novelty", "Change", "Progress", "Growth", "Expansion", "More", "Better", "Bigger", "Faster", "Rest", "Relaxation", "Vacation", "Retirement", "Leisure", "Free time", "Hobbies", "Recreation", "Entertainment", "Amusement"]
ALIGNED_MESSAGES = ["you are learning to let go", "a weight lifts off your shoulders", "you release what no longer serves you", "the grip loosens", "you surrender to what is", "horizons seem closer", "the sky slowly becomes clear", "the fog begins to lift", "clarity emerges from within", "you see things as they are", "the path reveals itself", "you breathe a little easier", "something inside you softens", "the noise fades away", "stillness finds you", "peace settles in your chest", "silence becomes a friend", "calm washes over you", "you remember who you are", "you are coming home to yourself", "your true self emerges", "you recognize your own voice", "you return to your center", "your heart grows lighter", "a smile finds your face", "burdens dissolve into nothing", "you float where you once sank", "you feel connected to everything", "boundaries soften", "you belong here", "the world welcomes you", "you arrive in this moment", "now is enough", "you need nothing else", "this breath is complete", "something new is growing", "space opens within you", "you expand beyond old limits", "possibility awakens", "the chains fall away", "you step into open air", "the horizon expands before you", "you taste what is real", "your feet find solid ground", "the storm passes through you", "you become transparent", "nothing sticks to you now", "you are already whole", "there is nothing to fix", "you were always enough", "the search ends here", "you stop running", "rest finds you at last", "you exhale completely", "tension melts away", "your shoulders drop", "your jaw unclenches", "warmth spreads through you", "you feel held by something larger", "trust returns", "hope whispers your name", "light enters through the cracks", "you are not alone", "everything is connected", "the walls come down", "you open like a flower", "your wings remember how to fly", "gravity loosens its grip", "you dance with uncertainty", "the unknown becomes a friend"]
MISALIGNED_MESSAGES = ["you must look within", "restate your purpose", "define who you are", "where is your will", "return to yourself", "come back to center", "you drift farther from clarity", "the path grows dim", "shadows lengthen around you", "the fog thickens", "you wander further from home", "seek what cannot be taken", "the answer is not there", "look deeper", "that is not the way", "freedom waits elsewhere", "try again with your heart", "listen more carefully", "is this what you truly need?", "will this set you free?", "what are you avoiding?", "what are you afraid to face?", "that path leads in circles", "you have been here before", "this is familiar pain", "the cage looks comfortable", "you are stronger than this", "trust yourself", "you know the answer", "the truth is simpler", "freedom cannot be bought", "you already have what you seek", "nothing external will fill this", "the void remains", "be patient with yourself", "there is no rush", "the journey continues", "another chance awaits", "this too shall pass", "let it go", "the weight is not yours to carry", "you are chasing shadows", "turn around", "the exit is behind you", "stop and breathe", "feel your feet on the ground", "where are you going so fast?", "pause here", "notice what you are doing", "is this familiar?", "you know how this ends", "choose differently this time", "the old ways do not work", "something must change", "that door leads nowhere", "you are building walls", "who are you hiding from?", "the mask is heavy", "put it down", "you do not need armor here", "soften your grip", "ease your hold", "what would happen if you stopped?", "nothing is chasing you", "you are safe to rest", "the race has no finish line", "there is no prize at the end", "you cannot win this game", "the rules are not real", "who wrote these rules?", "question everything", "start again", "begin where you are"]
QUESTIONS = ["what do you seek?", "what calls to you?", "what do you need?", "what would set you free?", "what does your heart want?", "what are you reaching for?", "what would bring you peace?", "what do you long for?", "what is missing?", "what would make you whole?", "what are you searching for?", "what does your soul crave?", "what would bring you home?", "what are you hungry for?", "what matters most right now?", "what would ease your mind?", "what do you truly desire?", "what calls from within?", "what would quiet the noise?", "what keeps you awake at night?", "what weighs on your heart?", "what are you holding onto?", "what are you afraid to lose?", "what would you chase to the end of the earth?", "what do you think you need?", "what have you been told you need?", "what would make everything okay?", "what are you running toward?", "what are you running from?", "what would fill the emptiness?", "what do you believe will save you?", "what are you waiting for?", "what would complete you?", "what do you envy in others?", "what do you wish you had?", "what do you think is the answer?"]
#def get_random_question(): # Return a random question
#    return random.choice(QUESTIONS)
def get_random_question(): # Return a seeded random question
    return session.rng.choice(QUESTIONS)
def get_aligned_message(): # Return a seeded message for choosing freedom
    return session.get_seeded_choice(ALIGNED_MESSAGES)
def get_misaligned_message(): # Return a seeded message for choosing distractions
    return session.get_seeded_choice(MISALIGNED_MESSAGES)
def get_choices(): # Generate 3 seeded choices including freedom
    options = session.rng.sample(DISTRACTIONS, 2)
    options.append("freedom")
    session.rng.shuffle(options)
    return options
def record_choice(choice_text, question_text=""): # Record a user choice for seed calculation
    session.add_choice(choice_text, question_text)
def print_session_summary(): # Print a summary of the session
    session.print_summary()
def reset_session(): # Reset session state for new run
    global session
    session = SessionState()
