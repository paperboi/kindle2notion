from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from kindle2notion.package_logger import logger


class Highlight(BaseModel):
    text: str
    page: Optional[int]
    location: tuple[int, int]
    date: datetime
    is_note: bool

    def make_aggregate_text(
        self, enable_location: bool, enable_highlight_date: bool
    ) -> str:
        aggregated_text = ""
        if self.is_note:
            aggregated_text += "> " + "NOTE: \n"

        aggregated_text += self.text + "\n"
        if enable_location:
            if self.page is not None:
                aggregated_text += "Page: " + str(self.page) + ", "
            aggregated_text += f"Location: {self.location[0]}-{self.location[1]}"
        if enable_highlight_date and (self.date is not None):
            aggregated_text += ", Date Added: " + self.date.strftime(
                "%d-%m-%Y, %H:%M:%S"
            )
        aggregated_text = aggregated_text.strip() + "\n\n"
        return aggregated_text


class Book(BaseModel):
    author: str
    title: str
    highlights: list[Highlight]

    def prune_subset_highlights(self):
        sorted_highlights = sorted(
            self.highlights, key=lambda x: (x.location[0], -x.location[1])
        )
        max_end_loc = 0

        filtered_highlights = []
        for highlight in sorted_highlights:
            end_loc = highlight.location[1]
            if max_end_loc < end_loc:
                filtered_highlights.append(highlight)
            max_end_loc = end_loc

        if len(filtered_highlights) < len(self.highlights):
            logger.info(
                f"Pruned highlights for [bold]{self.title} ({self.author})[/bold] from [red]{len(self.highlights)}[/red] -> [green]{len(filtered_highlights)}[/green]"
            )
        self.highlights = filtered_highlights

    @property
    def last_highlighted_date(self) -> datetime:
        assert len(self.highlights) > 0
        all_timestamps = [h.date for h in self.highlights]
        return max(all_timestamps)


class BookHeading(BaseModel):
    title: str
    href: str
    position: int = -1
