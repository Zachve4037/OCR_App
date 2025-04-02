import re
import Levenshtein
from src.OCRSystems import OCRSystem

class Tester:
    def __init__(self):
        pass

    def test_ocr(self, image_path, annotation):
        ocr_systems = OCRSystem()
        ocr_results = ocr_systems.perform_ocr(image_path)
        metrics = {}

        for system, result in ocr_results.items():
            cer = self.calculate_cer(annotation, result)
            wer = self.calculate_wer(annotation, result)
            metrics[system] = {
                "CER": cer,
                "WER": wer
            }
        return metrics

    def normalize_text(self, text):
        """Normalize text by lowercasing and removing extra spaces"""
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def calculate_cer(self, true_text, ocr_text):
        """Calculate Character Error Rate (CER)"""
        true_text = self.normalize_text(true_text)
        ocr_text = self.normalize_text(ocr_text)
        ref_chars = list(true_text)
        hyp_chars = list(ocr_text)
        levenshtein_distance = Levenshtein.distance(true_text, ocr_text)
        total_chars = len(ref_chars)
        cer = levenshtein_distance / total_chars if total_chars > 0 else 0
        return cer

    def calculate_wer(self, true_text, ocr_text):
        """Calculate Word Error Rate (WER)"""
        true_text = self.normalize_text(true_text)
        ocr_text = self.normalize_text(ocr_text)
        ref_words = true_text.split()
        hyp_words = ocr_text.split()
        levenshtein_distance = Levenshtein.distance(" ".join(ref_words), " ".join(hyp_words))
        total_words = len(ref_words)
        wer = levenshtein_distance / total_words if total_words > 0 else 0
        return wer
