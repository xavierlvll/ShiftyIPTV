from src.backend.db.session import AsyncSession
from src.backend.models.models import Channel, Program
import httpx
from typing import Any
from lxml import etree
from datetime import datetime

class EPGService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def import_xmltv(self, url: str) -> int:
        """
        Fetches and parses an XMLTV EPG file, updating the database with program information.
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                if response.status_code != 200:
                    raise Exception(f"Failed to fetch EPG: {response.status_code}")
                content = response.text
            except Exception as e:
                raise Exception(f"Error fetching EPG: {str(e)}")

        # Use lxml to parse the XML content
        try:
            parser = etree.XMLParser(recover=True)
            tree = ettree.fromstring(content.encode('utf-8'), parser=parser)
        except Exception as e:
            raise Exception(f"Failed to parse XMLTV: {str(e)}")

        channels_updated = 0
        
        # In a real implementation, we would find all channels that have an epg_id
        # and match them with the <program> elements in the XMLTV.
        # For now, we will use a simplified approach.

        # We'll iterate through all <program> elements in the XMLTV
        for program_element in tree.xpath("//program"):
            program_title = program_element.findtext("title")
            program_desc = program_element.findtext("desc")
            program_start_str = program_element.get("start")
            program_stop_str = program_element.get("stop")
            
            if not program_title or not program_start_str or not program_stop_str:
                continue

            # Parse date strings (XMLTV format: 20231118120000 +0000)
            try:
                # Simplified parsing for the example
                start_dt = datetime.strptime(program_start_str[:14], "%Y%m%d%H%M%S")
                stop_dt = datetime.strptime(program_stop_str[:14], "%Y%m%d%H%M%S")
            except ValueError:
                continue

            # Find the channel by matching epg_id in the XMLTV (if available)
            # In XMLTV, the <program> element often has a 'channel' attribute
            channel_id_in_xml = program_element.get("channel")
            
            # For this prototype, we'll assume we can match by a simplified logic
            # In reality, we'd match the channel ID from the XMLTV with our Channel.epg_id
            
            # Find channel in DB
            # For this prototype, we'll assume the channel_id_in_xml matches our Channel.epg_id
            from sqlalchemy import select
            from src.backend.models.models import Channel
            
            result = await self.db.execute(
                select(Channel).where(Channel.epg_id == channel_id_in_xml)
            )
            channel = result.scalars().first()
            
            if channel:
                new_program = Program(
                    channel_id=channel.id,
                    title=program_title,
                    description=program_desc,
                    start_time=start_dt,
                    end_name=stop_dt # Using the 'end_name' field as requested in the model
                )
                self.db.add(new_program)
                channels_updated += 1

        await self.db.commit()
        return channels_updated
