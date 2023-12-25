import json
from typing import Optional, List, Dict

from kafka import KafkaProducer, KafkaConsumer

from backbone.configs import config


class Kafka:
    __producer: Optional[KafkaProducer] = None
    __consumers: Dict[str, KafkaConsumer] = {}

    @classmethod
    def producer(cls):
        if cls.__producer is None:
            cls.__producer = KafkaProducer(
                bootstrap_servers=config.KAFKA_ADDRESS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            )

        return cls.__producer

    @classmethod
    def consumer(cls, group_id):
        if group_id not in cls.__consumers:
            c = KafkaConsumer(
                bootstrap_servers=config.KAFKA_ADDRESS,
                auto_offset_reset="earliest",
                group_id=str(group_id),
                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                enable_auto_commit=False,
            )
            cls.__consumers[group_id] = c
        return cls.__consumers[group_id]
