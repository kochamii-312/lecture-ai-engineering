from dataclasses import dataclass
from typing import List, Dict
import pandas as pd

@dataclass
class AnalysisResults:
    """分析結果を管理するクラス"""
    positive_comments: List[str]
    negative_comments: List[str]
    neutral_comments: List[str]
    
    lecture_content_comments: List[str]
    lecture_materials_comments: List[str]
    operation_comments: List[str]
    other_comments: List[str]
    
    dangerous_comments: List[tuple]
    
    def to_dataframe(self):
        """結果をDataFrameに変換"""
        all_comments = []
        
        # 感情ラベル付加
        for comment in self.positive_comments:
            all_comments.append({"comment": comment, "sentiment": "positive"})
        for comment in self.negative_comments:
            all_comments.append({"comment": comment, "sentiment": "negative"})
        for comment in self.neutral_comments:
            all_comments.append({"comment": comment, "sentiment": "neutral"})
        
        return pd.DataFrame(all_comments)
    
    def export_csv(self, filename="analysis_results.csv"):
        """CSV出力"""
        df = self.to_dataframe()
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        return filename