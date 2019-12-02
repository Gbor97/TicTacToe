
# Library imports
from pygameMenu.menu import Menu
import pygameMenu.config as _cfg
import pygameMenu.font as _fonts
import pygameMenu.locals as _locals
import pygameMenu
import os
import pygame


# noinspection PyProtectedMember
class TextMenu(Menu):
    """
    Menu with text lines.
    """

    def main_background():
        """
        Function used by menus, draw on background while menu is active.
        :return: None
        """
        global surface
        COLOR_BACKGROUND = (128, 0, 128)
        surface.fill(COLOR_BACKGROUND)

    def __init__(self,
                 surface,
                 window_width=600,
                 window_height=600,
                 font=pygameMenu.font.FONT_BEBAS,
                 title='Result',
                 draw_text_region_x=_cfg.TEXT_DRAW_X,
                 text_align=_locals.ALIGN_LEFT,
                 text_color=_cfg.TEXT_FONT_COLOR,
                 text_fontsize=_cfg.MENU_FONT_TEXT_SIZE,
                 text_margin=_cfg.TEXT_MARGIN,
                 bgfun=main_background,
                 **kwargs
                 ):
        os.environ['SDL_VIDEO_WINDOW_POS'] = '200,100'
        self.surface = pygame.display.set_mode((600,600))
        pygame.display.set_caption('Tic-tac-toe')
        """
        TextMenu constructor.
        :param surface: Pygame surface object
        :type surface: pygame.surface.SurfaceType
        :param window_width: Window width
        :type window_width: int
        :param window_height: Window height
        :type window_height: int
        :param font: Font file direction
        :type font: str
        :param title: Title of the Menu
        :type title: str
        :param draw_text_region_x: X-Axis drawing region of the text
        :type draw_text_region_x: int, float
        :param text_align: Text default alignment
        :type text_align: basestring
        :param text_color: Text color
        :type text_color: tuple
        :param text_fontsize: Text font size
        :type text_fontsize: int
        :param text_margin: Line margin
        :type text_margin: int
        :param kwargs: Aditional parameters
        """
        assert isinstance(draw_text_region_x, int) or \
               isinstance(draw_text_region_x, float)
        assert isinstance(text_align, str)
        assert isinstance(text_color, tuple)
        assert isinstance(text_fontsize, int)
        assert isinstance(text_margin, int)

        assert draw_text_region_x >= 0, 'draw_text_region_x of the text must be greater or equal than zero'
        assert text_fontsize > 0, 'text_fontsize must be greater than zero'
        assert text_margin >= 0, 'text_margin must be greater or equal than zero'

        # Super call
        super(TextMenu, self).__init__(surface,
                                       window_width,
                                       window_height,
                                       font,
                                       title,
                                       True, 
                                       bgfun,
                                       **kwargs)

        # Store configuration
        self._draw_text_region_x = draw_text_region_x
        self._font_textcolor = text_color
        self._font_textsize = text_fontsize
        self._text_align = text_align
        self._textdy = text_margin

        # Load font
        self._fonttext = _fonts.get_font(font, self._font_textsize)

        # Inner variables
        self._text = []

        # Position of text
        self._pos_text_x = int(self._width * (self._draw_text_region_x / 100.0)) + self._posx
        self._opt_posy -= self._textdy / 2 + self._font_textsize / 2


    def add_line(self, text):
        """
        Add line of text.
        :param text: Line text
        :type text: str
        :return: None
        """
        assert isinstance(text, str), 'line text must be a string'
        text = text.strip()
        self._text.append(text)
        dy = -self._font_textsize / 2 - self._textdy / 2
        self._opt_posy += dy

    def draw(self):
        """
        See upper class doc.
        """
        super(TextMenu, self).draw()

        # Draw text
        dy = 0
        for line in self._text:
            text = self._fonttext.render(line, 1, self._font_textcolor)
            text_width = text.get_size()[0]

            # Check text align
            if self._text_align == _locals.ALIGN_CENTER:
                text_dx = -int(self._width * (self._draw_text_region_x / 100.0)) + \
                          self._width / 2 - text_width / 2
            elif self._text_align == _locals.ALIGN_LEFT:
                text_dx = 0
            elif self._text_align == _locals.ALIGN_RIGHT:
                text_dx = -2 * int(self._width * (self._draw_text_region_x / 100.0)) \
                          - text_width + self._width
            else:
                text_dx = 0

            ycoords = self._opt_posy + self._textdy + dy * (self._font_textsize + self._textdy)
            ycoords -= self._font_textsize / 2

            self._surface.blit(text, (self._pos_text_x + text_dx, ycoords))
            dy += 1

    
