"""
Enhanced Diffie-Hellman Key Exchange Simulator
Professional UI/UX with Advanced Features & Modular Architecture
"""

import streamlit as st
import random
import time
import numpy as np
from typing import Tuple, Dict, Any, Optional
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from dataclasses import dataclass
from enum import Enum

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

class Theme(Enum):
    DARK = "dark"
    LIGHT = "light"
    CYBER = "cyber"
    NATURE = "nature"
    OCEAN = "ocean"

class SimulationMode(Enum):
    NORMAL = "normal"
    MITM = "mitm"

@dataclass
class SimulationConfig:
    prime: int
    base: int
    animation_speed: float
    theme: str = "dark"

# Complete theme color schemes
THEMES = {
    "dark": {
        "bg_primary": "#0f172a",
        "bg_secondary": "#1e293b",
        "bg_card": "rgba(30, 41, 59, 0.95)",
        "text_primary": "#f1f5f9",
        "text_secondary": "#94a3b8",
        "border": "rgba(148, 163, 184, 0.2)",
        "alice": "#ef4444",
        "alice_light": "rgba(239, 68, 68, 0.15)",
        "bob": "#3b82f6",
        "bob_light": "rgba(59, 130, 246, 0.15)",
        "eve": "#f59e0b",
        "eve_light": "rgba(245, 158, 11, 0.15)",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "info": "#3b82f6",
        "primary": "#667eea",
        "secondary": "#764ba2",
        "gradient_primary": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    },
    "light": {
        "bg_primary": "#f8fafc",
        "bg_secondary": "#ffffff",
        "bg_card": "rgba(255, 255, 255, 0.95)",
        "text_primary": "#1e293b",
        "text_secondary": "#64748b",
        "border": "rgba(0, 0, 0, 0.1)",
        "alice": "#dc2626",
        "alice_light": "rgba(220, 38, 38, 0.1)",
        "bob": "#2563eb",
        "bob_light": "rgba(37, 99, 235, 0.1)",
        "eve": "#ea580c",
        "eve_light": "rgba(234, 88, 12, 0.1)",
        "success": "#059669",
        "warning": "#d97706",
        "danger": "#dc2626",
        "info": "#2563eb",
        "primary": "#4f46e5",
        "secondary": "#7c3aed",
        "gradient_primary": "linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)",
    },
    "cyber": {
        "bg_primary": "#0a0a0f",
        "bg_secondary": "#0f0f1a",
        "bg_card": "rgba(15, 15, 26, 0.95)",
        "text_primary": "#00ff41",
        "text_secondary": "#00cc33",
        "border": "rgba(0, 255, 65, 0.2)",
        "alice": "#ff0055",
        "alice_light": "rgba(255, 0, 85, 0.15)",
        "bob": "#00ffff",
        "bob_light": "rgba(0, 255, 255, 0.15)",
        "eve": "#ff00ff",
        "eve_light": "rgba(255, 0, 255, 0.15)",
        "success": "#00ff41",
        "warning": "#ffff00",
        "danger": "#ff0055",
        "info": "#00ffff",
        "primary": "#00ff41",
        "secondary": "#ff00ff",
        "gradient_primary": "linear-gradient(135deg, #00ff41 0%, #00ccff 100%)",
    },
    "nature": {
        "bg_primary": "#1a3c2c",
        "bg_secondary": "#2d5a3c",
        "bg_card": "rgba(45, 90, 60, 0.95)",
        "text_primary": "#d4e6d4",
        "text_secondary": "#a8c9a8",
        "border": "rgba(168, 201, 168, 0.2)",
        "alice": "#ff8c42",
        "alice_light": "rgba(255, 140, 66, 0.15)",
        "bob": "#4c9f70",
        "bob_light": "rgba(76, 159, 112, 0.15)",
        "eve": "#ff6b6b",
        "eve_light": "rgba(255, 107, 107, 0.15)",
        "success": "#6bcf7f",
        "warning": "#ffa500",
        "danger": "#ff4757",
        "info": "#74b9ff",
        "primary": "#55efc4",
        "secondary": "#81ecec",
        "gradient_primary": "linear-gradient(135deg, #55efc4 0%, #81ecec 100%)",
    },
    "ocean": {
        "bg_primary": "#0a192f",
        "bg_secondary": "#173a6e",
        "bg_card": "rgba(23, 58, 110, 0.95)",
        "text_primary": "#ccf4ff",
        "text_secondary": "#8bc9e8",
        "border": "rgba(139, 201, 232, 0.2)",
        "alice": "#ff6b6b",
        "alice_light": "rgba(255, 107, 107, 0.15)",
        "bob": "#4ecdc4",
        "bob_light": "rgba(78, 205, 196, 0.15)",
        "eve": "#ffe66d",
        "eve_light": "rgba(255, 230, 109, 0.15)",
        "success": "#6bcf7f",
        "warning": "#ffa500",
        "danger": "#ff4757",
        "info": "#74b9ff",
        "primary": "#00cec9",
        "secondary": "#fd79a8",
        "gradient_primary": "linear-gradient(135deg, #00cec9 0%, #0984e3 100%)",
    }
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

@st.cache_data
def power_mod(base: int, exp: int, mod: int) -> int:
    """Efficient modular exponentiation using binary exponentiation"""
    result = 1
    base = base % mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod
    return result

def is_prime(n: int) -> bool:
    """Check if a number is prime"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def hex_to_rgba(hex_color: str, alpha: float = 0.3) -> str:
    """Convert hex color to rgba"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f'rgba({r}, {g}, {b}, {alpha})'

# ============================================================================
# CORE CRYPTOGRAPHY CLASSES
# ============================================================================

class DiffieHellmanUser:
    """Represents a user in Diffie-Hellman key exchange"""
    
    def __init__(self, name: str, prime: int, base: int):
        self.name = name
        self.prime = prime
        self.base = base
        self.private_key = None
        self.public_key = None
        self.shared_key = None
        self.received_public = None
        self.generate_keys()
    
    def generate_keys(self):
        """Generate new key pair"""
        self.private_key = random.randint(2, self.prime - 2)
        self.public_key = power_mod(self.base, self.private_key, self.prime)
        self.shared_key = None
        self.received_public = None
    
    def compute_shared_key(self, received_public_key: int) -> int:
        """Compute shared key from received public key"""
        self.received_public = received_public_key
        self.shared_key = power_mod(received_public_key, self.private_key, self.prime)
        return self.shared_key
    
    def reset(self):
        """Reset user to initial state"""
        self.generate_keys()

class MITMAttacker:
    """Represents a Man-in-the-Middle attacker (Eve)"""
    
    def __init__(self, name: str, prime: int, base: int):
        self.name = name
        self.prime = prime
        self.base = base
        self.private_key = None
        self.public_key = None
        self.shared_key_with_alice = None
        self.shared_key_with_bob = None
        self.alice_public = None
        self.bob_public = None
        self.generate_keys()
    
    def generate_keys(self):
        """Generate new key pair"""
        self.private_key = random.randint(2, self.prime - 2)
        self.public_key = power_mod(self.base, self.private_key, self.prime)
        self.shared_key_with_alice = None
        self.shared_key_with_bob = None
    
    def compute_shared_key_alice(self, alice_public: int) -> int:
        """Compute shared key with Alice"""
        self.alice_public = alice_public
        self.shared_key_with_alice = power_mod(alice_public, self.private_key, self.prime)
        return self.shared_key_with_alice
    
    def compute_shared_key_bob(self, bob_public: int) -> int:
        """Compute shared key with Bob"""
        self.bob_public = bob_public
        self.shared_key_with_bob = power_mod(bob_public, self.private_key, self.prime)
        return self.shared_key_with_bob
    
    def reset(self):
        """Reset attacker to initial state"""
        self.generate_keys()

# ============================================================================
# VISUALIZATION COMPONENTS
# ============================================================================

class VisualizationEngine:
    """Handles all visualization rendering"""
    
    @staticmethod
    def get_theme_colors():
        """Get current theme colors"""
        theme = st.session_state.get('current_theme', 'dark')
        return THEMES.get(theme, THEMES['dark'])
    
    @staticmethod
    def create_simple_explanation_diagram(alice, bob, attacker=None):
        """Create a simple, easy-to-understand diagram for laymen"""
        colors = VisualizationEngine.get_theme_colors()
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("Step 1: 🤫 Secret Keys", "Step 2: 📤 Public Keys", 
                          "Step 3: 🔄 Exchange", "Step 4: 🔐 Shared Secret"),
            vertical_spacing=0.2,
            horizontal_spacing=0.3
        )
        
        # Step 1: Secret Keys
        fig.add_trace(
            go.Bar(x=['Alice', 'Bob'], y=[alice.private_key, bob.private_key],
                  marker_color=[colors['alice'], colors['bob']],
                  text=[f"Secret: {alice.private_key}", f"Secret: {bob.private_key}"],
                  textposition='outside',
                  name='Private Keys'),
            row=1, col=1
        )
        
        # Step 2: Public Keys
        fig.add_trace(
            go.Bar(x=['Alice', 'Bob'], y=[alice.public_key, bob.public_key],
                  marker_color=[colors['alice'], colors['bob']],
                  text=[f"Public: {alice.public_key}", f"Public: {bob.public_key}"],
                  textposition='outside',
                  name='Public Keys'),
            row=1, col=2
        )
        
        # Step 3: Exchange visualization
        exchange_text = "⇄ Exchange Public Keys ⇄"
        fig.add_annotation(
            text=exchange_text,
            x=0.5, y=0.5,
            xref="x3", yref="y3",
            showarrow=False,
            font=dict(size=14, color=colors['primary']),
            row=2, col=1
        )
        
        # Step 4: Shared Secret
        if alice.shared_key:
            fig.add_trace(
                go.Bar(x=['Alice', 'Bob'], y=[alice.shared_key, bob.shared_key],
                      marker_color=[colors['alice'], colors['bob']],
                      text=[f"Shared: {alice.shared_key}", f"Shared: {bob.shared_key}"],
                      textposition='outside',
                      name='Shared Keys'),
                row=2, col=2
            )
        
        fig.update_layout(
            title="<b>🔐 How Diffie-Hellman Works - Simple Explanation</b>",
            showlegend=False,
            height=600,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor=colors['bg_secondary'],
            font=dict(color=colors['text_primary']),
            title_font=dict(size=18, color=colors['primary'])
        )
        
        fig.update_xaxes(title_text="Participants", row=1, col=1)
        fig.update_xaxes(title_text="Participants", row=1, col=2)
        fig.update_xaxes(title_text="Public Exchange Happens Here!", row=2, col=1)
        fig.update_xaxes(title_text="Result", row=2, col=2)
        
        fig.update_yaxes(title_text="Key Value", row=1, col=1)
        fig.update_yaxes(title_text="Key Value", row=1, col=2)
        
        return fig
    
    @staticmethod
    def create_network_diagram(alice, bob, attacker=None):
        """Create network architecture diagram"""
        colors = VisualizationEngine.get_theme_colors()
        fig = go.Figure()
        
        if attacker and attacker.shared_key_with_alice:
            # MITM scenario
            positions = {
                'Alice': (0, 2),
                'Eve': (1, 1),
                'Bob': (2, 2)
            }
            
            node_colors = {
                'Alice': colors['alice'],
                'Eve': colors['eve'],
                'Bob': colors['bob']
            }
            
            for node, (x, y) in positions.items():
                fig.add_trace(go.Scatter(
                    x=[x], y=[y],
                    mode='markers+text',
                    marker=dict(
                        size=80,
                        color=node_colors[node],
                        line=dict(color=colors['text_primary'], width=3),
                        symbol='circle'
                    ),
                    text=[node],
                    textposition="bottom center",
                    textfont=dict(color=colors['text_primary'], size=13, family='Arial Black'),
                    name=node,
                    showlegend=False,
                    hoverinfo='text',
                    hovertext=f'{node}<br>Status: Active'
                ))
            
            # Add connection lines with animation
            edges = [
                ((0, 2), (1, 1), f"📤 Alice → Eve<br>Public: {alice.public_key}", colors['alice']),
                ((1, 1), (2, 2), f"📤 Eve → Bob<br>Public: {attacker.public_key}", colors['bob']),
                ((2, 2), (1, 1), f"📤 Bob → Eve<br>Public: {bob.public_key}", colors['bob']),
                ((1, 1), (0, 2), f"📤 Eve → Alice<br>Public: {attacker.public_key}", colors['alice']),
            ]
            
            for (x1, y1), (x2, y2), hover_text, color in edges:
                fig.add_trace(go.Scatter(
                    x=[x1, x2],
                    y=[y1, y2],
                    mode='lines',
                    line=dict(color=color, width=3, dash='dot'),
                    hoverinfo='text',
                    hovertext=hover_text,
                    showlegend=False
                ))
        else:
            # Normal scenario
            positions = {
                'Alice': (0, 1),
                'Bob': (2, 1)
            }
            
            for node, (x, y) in positions.items():
                color = colors['alice'] if node == 'Alice' else colors['bob']
                fig.add_trace(go.Scatter(
                    x=[x], y=[y],
                    mode='markers+text',
                    marker=dict(
                        size=80,
                        color=color,
                        line=dict(color=colors['text_primary'], width=3),
                        symbol='circle'
                    ),
                    text=[node],
                    textposition="bottom center",
                    textfont=dict(color=colors['text_primary'], size=13, family='Arial Black'),
                    name=node,
                    showlegend=False
                ))
            
            # Secure channel
            fig.add_trace(go.Scatter(
                x=[0, 2],
                y=[1, 1],
                mode='lines',
                line=dict(color=colors['success'], width=4, dash='solid'),
                hoverinfo='text',
                hovertext='🔐 Secure Channel Established',
                showlegend=False
            ))
        
        fig.update_layout(
            title="<b>🔗 Network Communication Architecture</b>",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 2.5]),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 3]),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor=colors['bg_secondary'],
            height=450,
            showlegend=False,
            margin=dict(t=80, b=50, l=50, r=50),
            font=dict(color=colors['text_primary'], size=11),
            hovermode='closest',
            title_font=dict(size=16, color=colors['text_primary'])
        )
        
        return fig
    
    @staticmethod
    def create_comparison_chart(alice, bob, attacker=None):
        """Create key values comparison with simple labels"""
        colors = VisualizationEngine.get_theme_colors()
        categories = ['🔒 Private Key\n(Keep Secret!)', '📤 Public Key\n(Share Publicly)', '🔐 Shared Secret\n(Final Key)']
        
        if attacker and attacker.shared_key_with_alice:
            fig = go.Figure(data=[
                go.Bar(
                    name='👩 Alice',
                    x=categories,
                    y=[alice.private_key, alice.public_key, alice.shared_key or 0],
                    marker=dict(color=colors['alice'], line=dict(color=colors['text_primary'], width=1)),
                    text=[f"🤫 {alice.private_key}", f"📢 {alice.public_key}", f"🔐 {alice.shared_key or 'N/A'}"],
                    textposition='outside',
                    textfont=dict(size=10, color=colors['text_primary']),
                    hovertemplate='<b>Alice</b><br>%{x}: %{y}<extra></extra>'
                ),
                go.Bar(
                    name='👨 Bob',
                    x=categories,
                    y=[bob.private_key, bob.public_key, bob.shared_key or 0],
                    marker=dict(color=colors['bob'], line=dict(color=colors['text_primary'], width=1)),
                    text=[f"🤫 {bob.private_key}", f"📢 {bob.public_key}", f"🔐 {bob.shared_key or 'N/A'}"],
                    textposition='outside',
                    textfont=dict(size=10, color=colors['text_primary']),
                    hovertemplate='<b>Bob</b><br>%{x}: %{y}<extra></extra>'
                ),
                go.Bar(
                    name='👿 Eve (Attacker)',
                    x=categories,
                    y=[attacker.private_key, attacker.public_key, attacker.shared_key_with_alice or 0],
                    marker=dict(color=colors['eve'], line=dict(color=colors['text_primary'], width=1)),
                    text=[f"👿 {attacker.private_key}", f"🎭 {attacker.public_key}", f"⚠️ {attacker.shared_key_with_alice or 'N/A'}"],
                    textposition='outside',
                    textfont=dict(size=10, color=colors['text_primary']),
                    hovertemplate='<b>Eve</b><br>%{x}: %{y}<extra></extra>'
                )
            ])
        else:
            fig = go.Figure(data=[
                go.Bar(
                    name='👩 Alice',
                    x=categories,
                    y=[alice.private_key, alice.public_key, alice.shared_key or 0],
                    marker=dict(color=colors['alice'], line=dict(color=colors['text_primary'], width=1)),
                    text=[f"🤫 {alice.private_key}", f"📢 {alice.public_key}", f"🔐 {alice.shared_key or 'N/A'}"],
                    textposition='outside',
                    textfont=dict(size=10, color=colors['text_primary']),
                    hovertemplate='<b>Alice</b><br>%{x}: %{y}<extra></extra>'
                ),
                go.Bar(
                    name='👨 Bob',
                    x=categories,
                    y=[bob.private_key, bob.public_key, bob.shared_key or 0],
                    marker=dict(color=colors['bob'], line=dict(color=colors['text_primary'], width=1)),
                    text=[f"🤫 {bob.private_key}", f"📢 {bob.public_key}", f"🔐 {bob.shared_key or 'N/A'}"],
                    textposition='outside',
                    textfont=dict(size=10, color=colors['text_primary']),
                    hovertemplate='<b>Bob</b><br>%{x}: %{y}<extra></extra>'
                )
            ])
        
        fig.update_layout(
            barmode='group',
            title='<b>📊 What Each Person Knows (Simple View)</b>',
            xaxis_title='Type of Key',
            yaxis_title='Value',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor=colors['bg_secondary'],
            hovermode='x unified',
            font=dict(color=colors['text_primary'], size=11),
            showlegend=True,
            legend=dict(
                bgcolor=hex_to_rgba('#000000', 0.5),
                bordercolor=colors['primary'],
                borderwidth=1,
                font=dict(color=colors['text_primary'])
            ),
            height=500,
            margin=dict(t=100, b=80, l=80, r=50),
            title_font=dict(size=16, color=colors['text_primary'])
        )
        
        return fig
    
    @staticmethod
    def create_color_mixing_analogy():
        """Create a color mixing analogy for understanding DH"""
        colors = VisualizationEngine.get_theme_colors()
        
        fig = go.Figure()
        
        # Alice's secret color (Red)
        fig.add_shape(type="rect", x0=0, x1=1, y0=1.5, y1=2.5,
                     fillcolor="#ff4444", line_color="white", line_width=2)
        fig.add_annotation(x=0.5, y=2, text="Alice's<br>Secret Color", showarrow=False,
                          font=dict(size=12, color="white"), bgcolor="#ff4444")
        
        # Bob's secret color (Blue)
        fig.add_shape(type="rect", x0=2, x1=3, y0=1.5, y1=2.5,
                     fillcolor="#4444ff", line_color="white", line_width=2)
        fig.add_annotation(x=2.5, y=2, text="Bob's<br>Secret Color", showarrow=False,
                          font=dict(size=12, color="white"), bgcolor="#4444ff")
        
        # Common paint (Yellow) - Public base
        fig.add_shape(type="rect", x0=1, x1=2, y0=3.5, y1=4.5,
                     fillcolor="#ffdd44", line_color="white", line_width=2)
        fig.add_annotation(x=1.5, y=4, text="Common Paint<br>(Everyone knows)", showarrow=False,
                          font=dict(size=10, color="#333"), bgcolor="#ffdd44")
        
        # Alice mixes: Red + Yellow = Orange
        fig.add_shape(type="rect", x0=0, x1=1, y0=0, y1=1,
                     fillcolor="#ffaa44", line_color="white", line_width=2)
        fig.add_annotation(x=0.5, y=0.5, text="Alice sends:<br>Orange", showarrow=False,
                          font=dict(size=11, color="white"), bgcolor="#ffaa44")
        
        # Bob mixes: Blue + Yellow = Green
        fig.add_shape(type="rect", x0=2, x1=3, y0=0, y1=1,
                     fillcolor="#44ff44", line_color="white", line_width=2)
        fig.add_annotation(x=2.5, y=0.5, text="Bob sends:<br>Green", showarrow=False,
                          font=dict(size=11, color="white"), bgcolor="#44ff44")
        
        # Exchange arrows
        fig.add_annotation(x=1.5, y=0.5, text="⇄ Exchange<br>Mixtures ⇄", showarrow=False,
                          font=dict(size=12, color=colors['primary']))
        
        # Final shared secret
        fig.add_shape(type="rect", x0=1, x1=2, y0=-1.5, y1=-0.5,
                     fillcolor="#884444", line_color="white", line_width=3)
        fig.add_annotation(x=1.5, y=-1, text="🔐 Shared Secret!<br>Alice adds Blue → Brown<br>Bob adds Red → Brown", 
                          showarrow=False, font=dict(size=11, color="white"), bgcolor="#884444")
        
        fig.update_layout(
            title="<b>🎨 The Paint Mixing Analogy - How DH Really Works!</b>",
            xaxis=dict(range=[-0.5, 3.5], showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(range=[-2, 5], showgrid=False, zeroline=False, showticklabels=False),
            height=550,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor=colors['bg_secondary'],
            font=dict(color=colors['text_primary'])
        )
        
        return fig
    
    @staticmethod
    def create_cookie_jar_analogy():
        """Create a cookie jar analogy for better understanding"""
        colors = VisualizationEngine.get_theme_colors()
        
        fig = go.Figure()
        
        # Alice's secret recipe
        fig.add_shape(type="rect", x0=0, x1=1.2, y0=2.5, y1=3.5,
                     fillcolor=colors['alice'], line_color="white", line_width=2,
                     opacity=0.8)
        fig.add_annotation(x=0.6, y=3, text="🍪 Alice's<br>Secret Recipe", showarrow=False,
                          font=dict(size=11, color="white"))
        
        # Bob's secret recipe
        fig.add_shape(type="rect", x0=2.3, x1=3.5, y0=2.5, y1=3.5,
                     fillcolor=colors['bob'], line_color="white", line_width=2,
                     opacity=0.8)
        fig.add_annotation(x=2.9, y=3, text="🍪 Bob's<br>Secret Recipe", showarrow=False,
                          font=dict(size=11, color="white"))
        
        # Common ingredients
        fig.add_shape(type="rect", x0=1, x1=2, y0=1.8, y1=2.3,
                     fillcolor="#ffdd88", line_color="white", line_width=2)
        fig.add_annotation(x=1.5, y=2.05, text="🥚 Common<br>Ingredients", showarrow=False,
                          font=dict(size=9, color="#333"), bgcolor="#ffdd88")
        
        # Baked cookies (public)
        fig.add_shape(type="circle", x0=0.2, x1=1, y0=1, y1=1.6,
                     fillcolor="#d4a574", line_color="white", line_width=2)
        fig.add_annotation(x=0.6, y=1.3, text="Alice's<br>Cookie 🍪", showarrow=False,
                          font=dict(size=10, color="white"))
        
        fig.add_shape(type="circle", x0=2.5, x1=3.3, y0=1, y1=1.6,
                     fillcolor="#d4a574", line_color="white", line_width=2)
        fig.add_annotation(x=2.9, y=1.3, text="Bob's<br>Cookie 🍪", showarrow=False,
                          font=dict(size=10, color="white"))
        
        # Exchange arrows
        fig.add_annotation(x=1.7, y=1.3, text="⇄ Exchange<br>Cookies ⇄", showarrow=False,
                          font=dict(size=11, color=colors['primary']))
        
        # Final shared secret
        fig.add_shape(type="rect", x0=1, x1=2, y0=-0.5, y1=0.3,
                     fillcolor="#8B4513", line_color="white", line_width=3)
        fig.add_annotation(x=1.5, y=-0.1, text="🔐 Secret Shared Recipe!<br>Both can now make the SAME cookie", 
                          showarrow=False, font=dict(size=10, color="white"))
        
        fig.update_layout(
            title="<b>🍪 The Cookie Recipe Analogy</b>",
            xaxis=dict(range=[-0.5, 4], showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(range=[-1, 4], showgrid=False, zeroline=False, showticklabels=False),
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor=colors['bg_secondary'],
            font=dict(color=colors['text_primary'])
        )
        
        return fig
    
    @staticmethod
    def create_process_timeline(step: int):
        """Create interactive timeline"""
        colors = VisualizationEngine.get_theme_colors()
        phases = [
            ('🔑', 'Generate\nKeys', step > 1),
            ('📤', 'Exchange\nPublic Keys', step > 2),
            ('🧮', 'Compute\nShared Key', step > 3),
            ('✅', 'Verify &\nSecure', step >= 4),
        ]
        
        x_pos = list(range(len(phases)))
        colors_list = []
        texts = []
        
        for emoji, title, completed in phases:
            if completed:
                colors_list.append(colors['success'])
                texts.append(f"{emoji}<br>{title}<br>✅")
            elif phases.index((emoji, title, completed)) == step - 1:
                colors_list.append(colors['warning'])
                texts.append(f"{emoji}<br>{title}<br>⏳")
            else:
                colors_list.append('rgba(100, 116, 139, 0.3)')
                texts.append(f"{emoji}<br>{title}")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=x_pos,
            y=[0] * len(phases),
            mode='markers+text',
            marker=dict(
                size=90,
                color=colors_list,
                line=dict(color=colors['text_primary'], width=2),
                symbol='circle'
            ),
            text=texts,
            textposition='top center',
            textfont=dict(size=9, color=colors['text_primary'], family='Arial Black'),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        if len(phases) > 1:
            for i in range(len(phases) - 1):
                fig.add_trace(go.Scatter(
                    x=[i, i + 1],
                    y=[0, 0],
                    mode='lines',
                    line=dict(color=colors['primary'], width=3),
                    showlegend=False,
                    hoverinfo='skip'
                ))
        
        fig.update_layout(
            title='<b>⏱️ Process Timeline</b>',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1, 1]),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor=colors['bg_secondary'],
            height=320,
            showlegend=False,
            margin=dict(t=100, b=50, l=50, r=50),
            font=dict(color=colors['text_primary'], size=11),
            title_font=dict(size=16, color=colors['text_primary'])
        )
        
        return fig
    
    @staticmethod
    def create_security_level_gauge(prime):
        """Create a gauge showing security level"""
        colors = VisualizationEngine.get_theme_colors()
        
        # Calculate security level based on prime size
        if prime < 100:
            level = 20
            text = "⚠️ Low (Educational Only)"
            color = colors['warning']
        elif prime < 500:
            level = 50
            text = "📚 Medium (Learning)"
            color = colors['info']
        else:
            level = 80
            text = "🔒 High (Demonstration)"
            color = colors['success']
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=level,
            title={'text': "Security Level", 'font': {'color': colors['text_primary']}},
            delta={'reference': 100, 'increasing': {'color': colors['success']}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': colors['text_secondary']},
                'bar': {'color': color},
                'bgcolor': colors['bg_card'],
                'borderwidth': 2,
                'bordercolor': colors['border'],
                'steps': [
                    {'range': [0, 33], 'color': hex_to_rgba(colors['warning'], 0.3)},
                    {'range': [33, 66], 'color': hex_to_rgba(colors['info'], 0.3)},
                    {'range': [66, 100], 'color': hex_to_rgba(colors['success'], 0.3)}
                ],
                'threshold': {
                    'line': {'color': colors['danger'], 'width': 4},
                    'thickness': 0.75,
                    'value': level
                }
            }
        ))
        
        fig.add_annotation(
            x=0.5, y=-0.3,
            text=text,
            showarrow=False,
            font=dict(size=14, color=color)
        )
        
        fig.update_layout(
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor=colors['bg_secondary'],
            font=dict(color=colors['text_primary'])
        )
        
        return fig

# ============================================================================
# UI COMPONENTS
# ============================================================================

class UIComponents:
    """Handles UI rendering components"""
    
    @staticmethod
    def get_theme_colors():
        """Get current theme colors"""
        theme = st.session_state.get('current_theme', 'dark')
        return THEMES.get(theme, THEMES['dark'])
    
    @staticmethod
    def render_header():
        """Render enhanced header with theme support"""
        colors = UIComponents.get_theme_colors()
        
        st.markdown(f"""
            <style>
                @keyframes gradientBG {{
                    0% {{ background-position: 0% 50%; }}
                    50% {{ background-position: 100% 50%; }}
                    100% {{ background-position: 0% 50%; }}
                }}
                
                @keyframes slideDown {{
                    from {{ opacity: 0; transform: translateY(-30px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}
                
                .header-container {{
                    background: {colors['gradient_primary']};
                    background-size: 200% 200%;
                    animation: gradientBG 3s ease infinite, slideDown 0.6s ease-out;
                    padding: 2rem 2rem;
                    border-radius: 20px;
                    text-align: center;
                    margin-bottom: 2rem;
                    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
                }}
                
                .header-container h1 {{
                    font-size: 2.5em;
                    margin: 0;
                    color: white;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                    font-weight: 800;
                }}
                
                .header-container p {{
                    margin: 0.5rem 0 0 0;
                    font-size: 1.1em;
                    color: rgba(255,255,255,0.95);
                }}
            </style>
            <div class="header-container">
                <h1>🔐 Diffie-Hellman Key Exchange Simulator</h1>
                <p>Learn How Secure Communication Works - Made Simple!</p>
            </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_theme_selector():
        """Render theme selector in sidebar"""
        colors = UIComponents.get_theme_colors()
        
        st.sidebar.markdown("### 🎨 Theme Settings")
        
        themes = {
            "🌙 Dark": "dark",
            "☀️ Light": "light",
            "💻 Cyber": "cyber",
            "🌿 Nature": "nature",
            "🌊 Ocean": "ocean"
        }
        
        current_theme = st.session_state.get('current_theme', 'dark')
        current_theme_name = [name for name, value in themes.items() if value == current_theme][0]
        
        selected_theme = st.sidebar.selectbox(
            "Choose Your Theme",
            options=list(themes.keys()),
            index=list(themes.keys()).index(current_theme_name),
            key="theme_selector"
        )
        
        new_theme = themes[selected_theme]
        if new_theme != current_theme:
            st.session_state.current_theme = new_theme
            st.rerun()
        
        st.sidebar.markdown(f"""
            <div style="background: {colors['bg_secondary']}; padding: 10px; border-radius: 10px; margin-top: 10px; border: 1px solid {colors['border']};">
                <div style="display: flex; gap: 10px; justify-content: center;">
                    <div style="background: {colors['alice']}; width: 30px; height: 30px; border-radius: 50%;"></div>
                    <div style="background: {colors['bob']}; width: 30px; height: 30px; border-radius: 50%;"></div>
                    <div style="background: {colors['eve']}; width: 30px; height: 30px; border-radius: 50%;"></div>
                </div>
                <div style="text-align: center; margin-top: 8px; color: {colors['text_secondary']}; font-size: 0.8em;">
                    {selected_theme} Theme Active
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.sidebar.markdown("---")
    
    @staticmethod
    def render_participant_card(user, user_type: str):
        """Render participant information card"""
        colors = UIComponents.get_theme_colors()
        
        color_map = {
            "alice": (colors['alice'], "👩 Alice", "I keep my private key secret!"),
            "bob": (colors['bob'], "👨 Bob", "I keep my private key secret!"),
            "eve": (colors['eve'], "👿 Eve", "I'm the attacker! I try to intercept!"),
        }
        
        color, name, tip = color_map.get(user_type, (colors['info'], "User", ""))
        
        if user_type == "eve":
            shared_key_display = user.shared_key_with_alice if user.shared_key_with_alice else '⏳ Waiting...'
        else:
            shared_key_display = user.shared_key if user.shared_key else '⏳ Waiting...'
        
        st.markdown(f"""
            <div style="background: {colors['bg_card']}; border-radius: 15px; padding: 1rem; margin: 0.5rem 0; border: 2px solid {color};">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                    <div style="background: {color}; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px;">
                        {'🔴' if user_type == 'alice' else '🔵' if user_type == 'bob' else '🟡'}
                    </div>
                    <div>
                        <div style="font-size: 1.2em; font-weight: bold; color: {color};">{name}</div>
                        <div style="font-size: 0.8em; color: {colors['text_secondary']};">{tip}</div>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem;">
                    <div style="text-align: center; padding: 0.5rem; background: {colors['bg_secondary']}; border-radius: 8px;">
                        <div style="font-size: 0.7em; color: {colors['text_secondary']};">🔒 Private</div>
                        <div style="font-size: 1.1em; font-weight: bold;">{user.private_key}</div>
                    </div>
                    <div style="text-align: center; padding: 0.5rem; background: {colors['bg_secondary']}; border-radius: 8px;">
                        <div style="font-size: 0.7em; color: {colors['text_secondary']};">📤 Public</div>
                        <div style="font-size: 1.1em; font-weight: bold;">{user.public_key}</div>
                    </div>
                    <div style="text-align: center; padding: 0.5rem; background: {colors['bg_secondary']}; border-radius: 8px;">
                        <div style="font-size: 0.7em; color: {colors['text_secondary']};">🔐 Shared</div>
                        <div style="font-size: 1.1em; font-weight: bold;">{shared_key_display}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def initialize_session_state():
    """Initialize or reset session state"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.current_theme = 'dark'
        st.session_state.prime = 23
        st.session_state.base = 5
        st.session_state.animation_speed = 0.8
        st.session_state.step = 0
        st.session_state.mitm_active = False
        st.session_state.alice = DiffieHellmanUser("Alice", st.session_state.prime, st.session_state.base)
        st.session_state.bob = DiffieHellmanUser("Bob", st.session_state.prime, st.session_state.base)
        st.session_state.attacker = MITMAttacker("Eve", st.session_state.prime, st.session_state.base)

def setup_page_config():
    """Configure Streamlit page with theme support"""
    colors = THEMES.get(st.session_state.get('current_theme', 'dark'), THEMES['dark'])
    
    st.set_page_config(
        page_title="🔐 DH Key Exchange Simulator",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown(f"""
        <style>
            .main {{
                background: {colors['bg_primary']};
                color: {colors['text_primary']};
            }}
            
            .stApp {{
                background: {colors['bg_primary']};
            }}
            
            .stTabs [data-baseweb="tab-list"] {{
                gap: 1rem;
                background: transparent;
            }}
            
            .stTabs [data-baseweb="tab"] {{
                height: 45px;
                white-space: pre-wrap;
                background-color: {colors['bg_card']};
                border-radius: 10px;
                padding: 0 1.5rem;
                border: 1px solid {colors['border']};
                color: {colors['text_secondary']};
            }}
            
            .stTabs [aria-selected="true"] {{
                background: {colors['gradient_primary']};
                border-color: {colors['primary']};
                color: white;
            }}
            
            .stButton > button {{
                background: {colors['gradient_primary']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0.6rem 1.2rem;
                font-weight: 600;
                transition: all 0.3s ease;
            }}
            
            .stButton > button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            }}
            
            code {{
                background: {colors['bg_card']} !important;
                color: {colors['primary']} !important;
                padding: 0.2rem 0.4rem !important;
                border-radius: 4px !important;
            }}
            
            hr {{
                border-color: {colors['border']};
            }}
        </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render enhanced sidebar with theme support"""
    colors = THEMES.get(st.session_state.get('current_theme', 'dark'), THEMES['dark'])
    
    with st.sidebar:
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 1rem;">
                <div style="font-size: 2.5rem;">🔐</div>
                <div style="font-size: 1rem; font-weight: bold; color: {colors['primary']};">DH Key Exchange</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Theme selector
        UIComponents.render_theme_selector()
        
        st.markdown("### ⚙️ Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            prime_dict = {"23 (Small)": 23, "97 (Medium)": 97, "467 (Large)": 467, "1009 (XL)": 1009}
            prime_label = st.selectbox("🔢 Prime Number (p)", options=list(prime_dict.keys()))
            st.session_state.prime = prime_dict[prime_label]
        
        with col2:
            base_dict = {"2": 2, "3": 3, "5": 5, "7": 7}
            base_label = st.selectbox("🎯 Base Number (g)", options=list(base_dict.keys()))
            st.session_state.base = base_dict[base_label]
        
        st.markdown("---")
        
        st.session_state.animation_speed = st.slider("⏱️ Animation Speed", 0.3, 2.0, 0.8, 0.1)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Prime (p)", st.session_state.prime)
        with col2:
            st.metric("Base (g)", st.session_state.base)
        
        st.markdown("---")
        
        st.markdown("### 🎮 Controls")
        
        if st.button("🔄 New Simulation", use_container_width=True):
            st.session_state.alice = DiffieHellmanUser("Alice", st.session_state.prime, st.session_state.base)
            st.session_state.bob = DiffieHellmanUser("Bob", st.session_state.prime, st.session_state.base)
            st.session_state.attacker = MITMAttacker("Eve", st.session_state.prime, st.session_state.base)
            st.session_state.step = 0
            st.rerun()
        
        if st.button("🎲 Random Keys", use_container_width=True):
            st.session_state.alice.generate_keys()
            st.session_state.bob.generate_keys()
            st.session_state.attacker.generate_keys()
            st.rerun()
        
        st.markdown("---")
        
        mitm_toggle = st.checkbox("👿 Enable MITM Attack", value=st.session_state.mitm_active)
        
        if mitm_toggle != st.session_state.mitm_active:
            st.session_state.mitm_active = mitm_toggle
            st.session_state.step = 0
            st.rerun()
        
        # Educational tip
        st.markdown("---")
        st.markdown(f"""
            <div style="background: {colors['bg_card']}; padding: 1rem; border-radius: 10px;">
                <div style="font-size: 1.2em; margin-bottom: 0.5rem;">💡 Did You Know?</div>
                <div style="font-size: 0.85em; color: {colors['text_secondary']};">
                    Diffie-Hellman is used in HTTPS, SSH, and VPNs to secure over 95% of internet traffic!
                </div>
            </div>
        """, unsafe_allow_html=True)

def render_guide_tab():
    """Render comprehensive guide tab"""
    colors = THEMES.get(st.session_state.get('current_theme', 'dark'), THEMES['dark'])
    
    # Welcome section
    st.markdown(f"""
        <div style="background: {colors['gradient_primary']}; padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
            <div style="font-size: 3rem;">🎓</div>
            <h2 style="color: white; margin: 0;">Welcome to the Diffie-Hellman Guide!</h2>
            <p style="color: rgba(255,255,255,0.9);">Learn how two people can create a shared secret key, even with someone watching!</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Simple explanation with analogy
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div style="background: {colors['bg_card']}; padding: 1.5rem; border-radius: 10px; height: 100%;">
                <h3 style="color: {colors['primary']};">🎯 What problem does it solve?</h3>
                <p>Imagine Alice and Bob want to send secret messages, but Eve is eavesdropping on everything they say. How can they agree on a secret key without Eve knowing it?</p>
                <p><strong>The Magic:</strong> They can exchange information publicly, yet still end up with a shared secret that only they know!</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style="background: {colors['bg_card']}; padding: 1.5rem; border-radius: 10px; height: 100%;">
                <h3 style="color: {colors['primary']};">🔑 The Lockbox Analogy</h3>
                <p>1. Alice puts her secret in a lockbox and locks it with her lock<br>
                2. Bob puts his secret in a lockbox and locks it with his lock<br>
                3. They exchange lockboxes<br>
                4. Each adds their own lock to the other's box<br>
                5. Now both boxes have two locks - both can open them!</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Step by step with emojis
    st.markdown(f"""
        <h3 style="color: {colors['primary']}; text-align: center;">📝 How It Works - 4 Simple Steps</h3>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 2rem 0;">
            <div style="background: {colors['bg_card']}; padding: 1rem; border-radius: 10px; text-align: center;">
                <div style="font-size: 2rem;">1️⃣</div>
                <strong>Generate Secrets</strong>
                <div style="font-size: 0.85em; color: {colors['text_secondary']};">Alice & Bob pick random private numbers</div>
            </div>
            <div style="background: {colors['bg_card']}; padding: 1rem; border-radius: 10px; text-align: center;">
                <div style="font-size: 2rem;">2️⃣</div>
                <strong>Create Public Keys</strong>
                <div style="font-size: 0.85em; color: {colors['text_secondary']};">They calculate public keys from private ones</div>
            </div>
            <div style="background: {colors['bg_card']}; padding: 1rem; border-radius: 10px; text-align: center;">
                <div style="font-size: 2rem;">3️⃣</div>
                <strong>Exchange Publicly</strong>
                <div style="font-size: 0.85em; color: {colors['text_secondary']};">They send public keys to each other</div>
            </div>
            <div style="background: {colors['bg_card']}; padding: 1rem; border-radius: 10px; text-align: center;">
                <div style="font-size: 2rem;">4️⃣</div>
                <strong>Create Shared Secret</strong>
                <div style="font-size: 0.85em; color: {colors['text_secondary']};">Both compute the same secret key!</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Interactive example
    st.markdown(f"""
        <div style="background: {colors['bg_card']}; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
            <h3 style="color: {colors['primary']};">🧪 Try It Yourself!</h3>
            <p>Use the sidebar to change numbers and see how the shared key changes. Watch the Visualizations tab to see it in action!</p>
            <p><strong>Current numbers:</strong> p={st.session_state.prime}, g={st.session_state.base}</p>
            <p>⚠️ <strong>Note:</strong> Real cryptography uses HUGE primes (hundreds of digits long), but we use small numbers for learning.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # MITM warning
    if not st.session_state.mitm_active:
        st.markdown(f"""
            <div style="background: {hex_to_rgba(colors['warning'], 0.2)}; padding: 1.5rem; border-radius: 10px; border-left: 5px solid {colors['warning']}; margin: 1rem 0;">
                <h3 style="color: {colors['warning']}; margin: 0;">⚠️ Security Warning</h3>
                <p>Diffie-Hellman alone doesn't prevent "Man-in-the-Middle" attacks. Try enabling MITM mode to see how an attacker can intercept the keys!</p>
            </div>
        """, unsafe_allow_html=True)

def render_stepwise_tab():
    """Render step-by-step interactive tab"""
    colors = THEMES.get(st.session_state.get('current_theme', 'dark'), THEMES['dark'])
    
    st.markdown("### 🔄 Interactive Walkthrough")
    st.markdown("Follow these steps to see how the key exchange works!")
    
    st.markdown("---")
    
    # Step buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("1️⃣ Generate Keys", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    
    with col2:
        if st.button("2️⃣ Exchange Keys", use_container_width=True):
            st.session_state.step = 2
            st.rerun()
    
    with col3:
        if st.button("3️⃣ Compute Shared", use_container_width=True):
            st.session_state.step = 3
            st.rerun()
    
    with col4:
        if st.button("4️⃣ Verify", use_container_width=True):
            st.session_state.step = 4
            st.rerun()
    
    # Progress
    progress_percent = (st.session_state.step / 4) * 100
    st.progress(st.session_state.step / 4)
    st.caption(f"📊 Progress: {progress_percent:.0f}%")
    
    st.markdown("---")
    
    # Step details
    if st.session_state.step >= 1:
        st.markdown("### ✅ Step 1: Generate Secret Keys")
        st.markdown("Each person creates a **private key** (kept secret) and a **public key** (shared openly)")
        
        col1, col2 = st.columns(2)
        with col1:
            UIComponents.render_participant_card(st.session_state.alice, "alice")
        with col2:
            UIComponents.render_participant_card(st.session_state.bob, "bob")
        
        if st.session_state.mitm_active:
            st.markdown("#### 👿 Attacker is listening!")
            UIComponents.render_participant_card(st.session_state.attacker, "eve")
    
    if st.session_state.step >= 2:
        st.markdown("---")
        st.markdown("### 📤 Step 2: Exchange Public Keys")
        
        if st.session_state.mitm_active:
            st.warning("⚠️ MITM Attack in Progress!")
            st.write("Eve is intercepting the keys and replacing them with her own!")
            st.write("- Alice thinks she's sending to Bob → Eve intercepts")
            st.write("- Bob thinks he's sending to Alice → Eve intercepts")
            st.write("- Both are actually talking to Eve without knowing!")
        else:
            st.success("✅ Secure Exchange")
            st.write("Alice and Bob exchange their public keys safely!")
            st.write("- 📤 Alice sends her public key to Bob")
            st.write("- 📤 Bob sends his public key to Alice")
            st.write("- 🔒 Private keys remain secret")
    
    if st.session_state.step >= 3:
        st.markdown("---")
        st.markdown("### 🧮 Step 3: Compute the Shared Secret")
        st.markdown("Using the received public key and their own private key, each person calculates the same shared secret!")
        
        if st.session_state.mitm_active:
            alice_shared = st.session_state.alice.compute_shared_key(st.session_state.attacker.public_key)
            bob_shared = st.session_state.bob.compute_shared_key(st.session_state.attacker.public_key)
            eve_alice = st.session_state.attacker.compute_shared_key_alice(st.session_state.alice.public_key)
            eve_bob = st.session_state.attacker.compute_shared_key_bob(st.session_state.bob.public_key)
            
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"🔐 Alice's Shared Key: **{alice_shared}**")
            with col2:
                st.success(f"🔐 Bob's Shared Key: **{bob_shared}**")
            
            st.warning(f"👿 Eve now has two keys: {eve_alice} (with Alice) and {eve_bob} (with Bob)")
        else:
            alice_shared = st.session_state.alice.compute_shared_key(st.session_state.bob.public_key)
            bob_shared = st.session_state.bob.compute_shared_key(st.session_state.alice.public_key)
            
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"🔐 Alice's Shared Key: **{alice_shared}**")
            with col2:
                st.success(f"🔐 Bob's Shared Key: **{bob_shared}**")
    
    if st.session_state.step >= 4:
        st.markdown("---")
        
        if st.session_state.mitm_active:
            if st.session_state.alice.shared_key != st.session_state.bob.shared_key:
                st.error("🚨 ATTACK SUCCESSFUL! Keys Don't Match!")
                st.write("**What happened?**")
                st.write(f"- Alice thinks the secret is: {st.session_state.alice.shared_key}")
                st.write(f"- Bob thinks the secret is: {st.session_state.bob.shared_key}")
                st.write("- Eve knows BOTH secrets!")
                st.write("")
                st.write("**Eve can now:**")
                st.write("- Read all messages")
                st.write("- Modify messages")
                st.write("- Impersonate either person")
                st.write("")
                st.write("**💡 Prevention:** Use authentication (digital signatures, certificates) to verify identities.")
        else:
            if st.session_state.alice.shared_key == st.session_state.bob.shared_key:
                st.success("🎉 SUCCESS! Shared Secret Established!")
                st.write(f"**Both Alice and Bob have the same secret key: {st.session_state.alice.shared_key}**")
                st.write("")
                st.write("Even though Eve saw everything they sent, she can't figure out the secret key!")
                st.write("")
                st.write("This key can now be used to encrypt messages between them.")

def render_mathematics_tab():
    """Render mathematics explanation tab"""
    colors = THEMES.get(st.session_state.get('current_theme', 'dark'), THEMES['dark'])
    
    st.markdown(f"""
        <div style="background: {colors['bg_card']}; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
            <h3 style="color: {colors['primary']};">🧮 The Math Behind the Magic</h3>
            <p>Don't worry - the math looks scary, but the idea is simple! It's based on a special property of exponents.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div style="background: {colors['bg_card']}; padding: 1.5rem; border-radius: 10px;">
                <h4>🔢 With Our Numbers:</h4>
                <p><strong>Public Information (Everyone knows this):</strong></p>
                <ul>
                    <li>Prime number (p) = <code>{st.session_state.prime}</code></li>
                    <li>Base (g) = <code>{st.session_state.base}</code></li>
                </ul>
                <p><strong>Alice's Secret:</strong> a = <code>{st.session_state.alice.private_key}</code></p>
                <p><strong>Bob's Secret:</strong> b = <code>{st.session_state.bob.private_key}</code></p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style="background: {colors['bg_card']}; padding: 1.5rem; border-radius: 10px;">
                <h4>✨ The Magic Formula:</h4>
                <p><strong>Alice computes:</strong> A = g^a mod p = <code>{st.session_state.alice.public_key}</code></p>
                <p><strong>Bob computes:</strong> B = g^b mod p = <code>{st.session_state.bob.public_key}</code></p>
                <p><strong>They exchange A and B</strong> (everyone sees these!)</p>
                <p><strong>Alice computes:</strong> K = B^a mod p</p>
                <p><strong>Bob computes:</strong> K = A^b mod p</p>
                <p><strong>They both get:</strong> K = <code>{st.session_state.alice.shared_key if st.session_state.alice.shared_key else 'Not yet computed'}</code></p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown(f"""
        <div style="background: {colors['bg_card']}; padding: 1.5rem; border-radius: 10px;">
            <h3 style="color: {colors['primary']};">🎯 Why This is Secure</h3>
            <p>Even if Eve knows p, g, A, and B, she can't figure out the shared key because:</p>
            <ul>
                <li>To get K, she would need to know a or b</li>
                <li>Finding a from A = g^a mod p is extremely hard (Discrete Log Problem)</li>
                <li>With real numbers (hundreds of digits), it would take billions of years to solve!</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

def render_visualization_tab():
    """Render complete visualization tab"""
    colors = THEMES.get(st.session_state.get('current_theme', 'dark'), THEMES['dark'])
    
    st.markdown(f"""
        <div style="background: {colors['bg_card']}; padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem; text-align: center;">
            <h2 style="color: {colors['primary']}; margin: 0;">📊 Interactive Visualizations</h2>
            <p style="margin: 0.5rem 0 0 0;">See the Diffie-Hellman key exchange in action!</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different visualizations
    viz_tab1, viz_tab2, viz_tab3, viz_tab4, viz_tab5, viz_tab6 = st.tabs([
        "🎨 Simple View", "🔗 Network", "📊 Comparison", "🎬 Animation", "🎨 Paint Mix", "🍪 Cookie Jar"
    ])
    
    with viz_tab1:
        st.markdown("### 🎨 How the Process Works - Step by Step")
        fig_simple = VisualizationEngine.create_simple_explanation_diagram(
            st.session_state.alice, st.session_state.bob,
            st.session_state.attacker if st.session_state.mitm_active else None
        )
        st.plotly_chart(fig_simple, use_container_width=True)
        
        # Add explanation
        st.markdown(f"""
            <div style="background: {colors['bg_secondary']}; padding: 1rem; border-radius: 10px; margin-top: 1rem;">
                <p><strong>📖 What you're seeing:</strong></p>
                <ul>
                    <li><strong>Step 1:</strong> Alice and Bob create their secret (private) keys</li>
                    <li><strong>Step 2:</strong> They create public keys from their secret keys</li>
                    <li><strong>Step 3:</strong> They exchange public keys (Eve can see these!)</li>
                    <li><strong>Step 4:</strong> Both calculate the SAME shared secret key!</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with viz_tab2:
        st.markdown("### 🔗 Network Communication Flow")
        fig_network = VisualizationEngine.create_network_diagram(
            st.session_state.alice, st.session_state.bob,
            st.session_state.attacker if st.session_state.mitm_active else None
        )
        st.plotly_chart(fig_network, use_container_width=True)
        
        # MITM explanation
        if st.session_state.mitm_active:
            st.warning("⚠️ MITM Attack Active! Eve is intercepting all communications between Alice and Bob.")
        else:
            st.success("✅ Secure Channel Active! Alice and Bob have established a secure communication channel.")
    
    with viz_tab3:
        st.markdown("### 📊 Key Comparison Chart")
        fig_comparison = VisualizationEngine.create_comparison_chart(
            st.session_state.alice, st.session_state.bob,
            st.session_state.attacker if st.session_state.mitm_active else None
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Live status
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.session_state.alice.shared_key:
                st.metric("🔐 Alice's Key", st.session_state.alice.shared_key)
            else:
                st.info("Complete steps 1-4")
        
        with col2:
            if st.session_state.bob.shared_key:
                st.metric("🔐 Bob's Key", st.session_state.bob.shared_key)
            else:
                st.info("Complete steps 1-4")
        
        with col3:
            if st.session_state.alice.shared_key and st.session_state.bob.shared_key:
                if st.session_state.alice.shared_key == st.session_state.bob.shared_key:
                    st.success("✅ Keys Match! Secure!")
                else:
                    st.error("❌ Keys Don't Match!")
    
    with viz_tab4:
        st.markdown("### 🎬 Interactive Visualization")
        st.info("This visualization shows the key exchange process interactively!")
        
        # Create a simple animation showing the exchange
        fig_anim = go.Figure()
        
        fig_anim.add_trace(go.Scatter(
            x=[0, 2],
            y=[1, 1],
            mode='markers+text',
            marker=dict(size=60, color=[colors['alice'], colors['bob']]),
            text=['Alice', 'Bob'],
            textposition='top center',
            textfont=dict(color=colors['text_primary']),
            showlegend=False
        ))
        
        fig_anim.update_layout(
            title="Key Exchange Process",
            xaxis=dict(range=[-1, 3], showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(range=[0, 2], showgrid=False, zeroline=False, showticklabels=False),
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor=colors['bg_secondary'],
            font=dict(color=colors['text_primary'])
        )
        
        st.plotly_chart(fig_anim, use_container_width=True)
    
    with viz_tab5:
        st.markdown("### 🎨 The Paint Mixing Analogy (Best Explanation!)")
        fig_paint = VisualizationEngine.create_color_mixing_analogy()
        st.plotly_chart(fig_paint, use_container_width=True)
        
        st.markdown("""
            **🎨 How the Paint Mixing Analogy Works:**
            1. **Step 1:** Alice has a 🔴 SECRET red color (her private key)
            2. **Step 2:** Bob has a 🔵 SECRET blue color (his private key)
            3. **Step 3:** Everyone knows the 🟡 common yellow paint (public base)
            4. **Step 4:** Alice mixes Red + Yellow = 🟠 Orange (her public key)
            5. **Step 5:** Bob mixes Blue + Yellow = 🟢 Green (his public key)
            6. **Step 6:** They exchange Orange and Green (Eve sees these!)
            7. **Step 7:** Alice adds Bob's Green to her Red = 🤎 Brown
            8. **Step 8:** Bob adds Alice's Orange to his Blue = 🤎 Brown
            9. **✨ MAGIC:** Both get the SAME Brown color without sharing their secret colors!
            
            **🔐 This is EXACTLY how Diffie-Hellman works** - but with mathematical operations instead of paint mixing!
            
            Eve sees Orange and Green, but can't figure out the final Brown without knowing Red or Blue!
        """)
    
    with viz_tab6:
        st.markdown("### 🍪 The Cookie Recipe Analogy")
        fig_cookie = VisualizationEngine.create_cookie_jar_analogy()
        st.plotly_chart(fig_cookie, use_container_width=True)
        
        st.markdown("""
            **🍪 Another way to think about it:**
            - Alice has a secret cookie recipe ingredient
            - Bob has a different secret cookie ingredient
            - They both know the common ingredients (flour, sugar, eggs)
            - Each bakes a cookie with their secret + common ingredients
            - They exchange cookies
            - Each adds their OWN secret ingredient to the OTHER's cookie
            - ✨ Both end up with cookies that taste the SAME!
            
            Eve can see the cookies but can't figure out the final taste without knowing both secret ingredients!
        """)
    
    # Timeline and Security Level
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⏱️ Process Timeline")
        fig_timeline = VisualizationEngine.create_process_timeline(st.session_state.step)
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    with col2:
        st.markdown("### 🔒 Security Level")
        fig_gauge = VisualizationEngine.create_security_level_gauge(st.session_state.prime)
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.caption("Note: Real cryptography uses primes with hundreds of digits!")

def main():
    """Main application"""
    setup_page_config()
    initialize_session_state()
    
    UIComponents.render_header()
    render_sidebar()
    
    st.markdown("---")
    
    # Reorganized tabs: Guide first, Visualizations last
    tab_guide, tab_step, tab_math, tab_vis = st.tabs([
        "📚 Guide (Start Here!)",
        "📝 Step-by-Step",
        "🧮 Mathematics",
        "📊 Visualizations"
    ])
    
    with tab_guide:
        render_guide_tab()
    
    with tab_step:
        render_stepwise_tab()
    
    with tab_math:
        render_mathematics_tab()
    
    with tab_vis:
        render_visualization_tab()
    
    # Footer
    colors = THEMES.get(st.session_state.get('current_theme', 'dark'), THEMES['dark'])
    st.markdown(f"""
        <hr>
        <div style="text-align: center; color: {colors['text_secondary']}; padding: 2rem 0; font-size: 0.9em;">
            🔐 Diffie-Hellman Key Exchange Simulator | Educational Purpose
            <br>
            Built with Streamlit | Learn cryptography the fun way!
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()