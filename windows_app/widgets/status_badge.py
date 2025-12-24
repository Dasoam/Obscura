# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 Obscura Contributors

"""
Status Badge Widget
Premium status indicator badges for the header bar
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QEnterEvent


class StatusBadge(QWidget):
    """Modern status badge with icon and hover effects"""
    
    def __init__(
        self, 
        icon: str, 
        label: str, 
        value: str, 
        accent_color: str = "#58a6ff",
        parent=None
    ):
        super().__init__(parent)
        self._icon = icon
        self._label = label
        self._accent_color = accent_color
        
        # Calculate background color (darker version of accent)
        self._bg_color = self._get_bg_color(accent_color)
        self._hover_bg = self._get_hover_bg(accent_color)
        
        self._is_hovered = False
        self._setup_ui(value)
    
    def _get_bg_color(self, accent: str) -> str:
        """Get a darker background based on accent color"""
        color_map = {
            "#3fb950": "#1a2f1a",  # Green
            "#f0883e": "#2d2004",  # Orange  
            "#58a6ff": "#0d1f37",  # Blue
        }
        return color_map.get(accent, "#161b22")
    
    def _get_hover_bg(self, accent: str) -> str:
        """Get hover background color"""
        color_map = {
            "#3fb950": "#243d24",  # Green
            "#f0883e": "#3d2a08",  # Orange
            "#58a6ff": "#142847",  # Blue
        }
        return color_map.get(accent, "#21262d")
    
    def _setup_ui(self, value: str):
        self.setAttribute(Qt.WA_Hover, True)
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 6, 12, 6)
        layout.setSpacing(6)
        
        # Icon
        self._icon_lbl = QLabel(self._icon)
        self._icon_lbl.setStyleSheet("""
            font-size: 12px;
            background: transparent;
        """)
        layout.addWidget(self._icon_lbl)
        
        # Text: "Label: Value"
        self._text_lbl = QLabel(f"{self._label}: {value}")
        self._text_lbl.setStyleSheet(f"""
            color: {self._accent_color};
            font-size: 12px;
            font-weight: 600;
            background: transparent;
        """)
        layout.addWidget(self._text_lbl)
        
        self.setLayout(layout)
        self._apply_style()
    
    def _apply_style(self):
        """Apply widget style based on hover state"""
        bg = self._hover_bg if self._is_hovered else self._bg_color
        border_color = self._accent_color if self._is_hovered else "#30363d"
        
        self.setStyleSheet(f"""
            StatusBadge {{
                background: {bg};
                border: 1px solid {border_color};
                border-radius: 6px;
            }}
        """)
    
    def set_value(self, value: str):
        """Update the displayed value"""
        try:
            self._text_lbl.setText(f"{self._label}: {value}")
        except RuntimeError:
            # Widget may have been deleted
            pass
    
    def enterEvent(self, event: QEnterEvent):
        self._is_hovered = True
        self._apply_style()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self._is_hovered = False
        self._apply_style()
        super().leaveEvent(event)
