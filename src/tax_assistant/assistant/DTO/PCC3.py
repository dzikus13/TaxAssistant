from dataclasses import dataclass,field,asdict
from typing import Optional
import json


@dataclass
class Dane:
    p1: int
    p4: str
    p9: str
    p11: str
    p12: str
    p13: str
    p14: str
    p16: int
    p18: str
    p19: str
    p23: str
    p26: str
    p15: Optional[str] = field(default=None)
    p17: Optional[str] = field(default= None)
    

    @classmethod
    def from_json(cls, json_string: str):
        data = json.loads(json_string)
        return cls(
            p1=data['P_1'],
            p4=data['P_4'],
            p9=data['P_9'],
            p11=data['P_11'],
            p12=data['P_12'],
            p13=data['P_13'],
            p14=data['P_14'],
            p16=data['P_16'],
            p18=data['P_18'],
            p19=data['P_19'],
            p23=data['P_23'],
            p26=data['P_26'],
            p15=data.get('P_15'),  
            p17=data.get('P_17')   
        )
        
           
    def to_json(self):
        return json.dumps(asdict(self))