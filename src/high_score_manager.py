# ==========================
#   High Score Manager Module
#   Simulates NVM storage for persistent high scores.
# ==========================

class HighScoreManager:
    
    DEFAULT_SCORES = [
        {"score": 18, "initials": "LYA"},
        {"score": 16, "initials": "PNT"},
        {"score": 11, "initials": "JOE"},
    ]
    
    NVM_KEY_PREFIX = "HS" 

    def __init__(self, hardware):
        self.hardware = hardware
        self.high_scores = self._load_scores()

    def _serialize_scores(self):
        parts = []
        for entry in self.high_scores:
            score = int(entry.get("score", 0))
            initials = str(entry.get("initials", "---"))[:3]
            parts.append(f"{score},{initials}")
        return ";".join(parts)

    def _deserialize_scores(self, data_string):
        if not data_string:
            return self.DEFAULT_SCORES
        
        scores = []
        try:
            entries = data_string.split(";")
            for entry in entries:
                if "," in entry:
                    score_str, initials = entry.split(",", 1)
                    score = int(score_str.strip())
                    initials = initials.strip().upper()
                    scores.append({"score": score, "initials": initials})
        except Exception as e:
            print(f"Error deserializing scores: {e}. Using defaults.")
            return self.DEFAULT_SCORES
            
        while len(scores) < 3:
            scores.append(self.DEFAULT_SCORES[len(scores)])
            
        return scores[:3]

    def _load_scores(self):
        return self.DEFAULT_SCORES

    def _save_scores(self):
        print(f"Scores saved (Simulated NVM): {self._serialize_scores()}")


    def check_and_insert_score(self, new_score):
        if new_score <= 0:
            return -1 
        if new_score > self.high_scores[2]["score"]:
            insert_index = -1
            for i in range(3):
                if new_score >= self.high_scores[i]["score"]:
                    insert_index = i
                    break
            
            self.high_scores.insert(insert_index, {"score": new_score, "initials": "___"})
            self.high_scores.pop()
            
            return insert_index
        
        return -1

    def update_initials(self, index, initials):
        if 0 <= index < 3:
            self.high_scores[index]["initials"] = initials.upper()
            self._save_scores()

    def get_scores(self):
        return self.high_scores
