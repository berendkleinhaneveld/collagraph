"""Tests for PySide widget types showcased in tests/data/pyside/ .cgx files.

These tests import .cgx components that exercise various QWidget subclasses
and verify that the widget hierarchy is created correctly by the renderer.
"""

import pytest

PySide6 = pytest.importorskip("PySide6")

from PySide6 import QtCore, QtGui, QtWidgets

import collagraph as cg


def get_current_window(app):
    """Returns the first QMainWindow among top-level widgets."""
    windows = [
        widget
        for widget in app.topLevelWidgets()
        if isinstance(widget, QtWidgets.QMainWindow)
    ]
    assert len(windows) <= 1
    return windows[0] if windows else None


# ---------------------------------------------------------------------------
# Form Inputs
# ---------------------------------------------------------------------------


class TestFormInputs:
    def test_form_inputs_render(self, qapp, qtbot):
        """Test that form input widgets are created and placed in the hierarchy."""
        from tests.data.pyside.form_inputs import FormInputs

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(FormInputs, container)

        def check_form_group():
            group = container.findChild(QtWidgets.QGroupBox, "form-group")
            assert group is not None
            layout = group.layout()
            assert isinstance(layout, QtWidgets.QFormLayout)

        qtbot.waitUntil(check_form_group, timeout=500)

    def test_form_inputs_lineedit(self, qapp, qtbot):
        """Test that the name LineEdit is present."""
        from tests.data.pyside.form_inputs import FormInputs

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(FormInputs, container)

        def check_lineedit():
            lineedit = container.findChild(QtWidgets.QLineEdit, "name-input")
            assert lineedit is not None

        qtbot.waitUntil(check_lineedit, timeout=500)

    def test_form_inputs_spinbox(self, qapp, qtbot):
        """Test that the age SpinBox is present with correct range."""
        from tests.data.pyside.form_inputs import FormInputs

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(FormInputs, container)

        def check_spinbox():
            spinbox = container.findChild(QtWidgets.QSpinBox, "age-input")
            assert spinbox is not None
            assert spinbox.minimum() == 0
            assert spinbox.maximum() == 150

        qtbot.waitUntil(check_spinbox, timeout=500)

    def test_form_inputs_double_spinbox(self, qapp, qtbot):
        """Test that the height DoubleSpinBox is present."""
        from tests.data.pyside.form_inputs import FormInputs

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(FormInputs, container)

        def check_double_spinbox():
            spinbox = container.findChild(QtWidgets.QDoubleSpinBox, "height-input")
            assert spinbox is not None
            assert spinbox.suffix() == " m"

        qtbot.waitUntil(check_double_spinbox, timeout=500)

    def test_form_inputs_combobox(self, qapp, qtbot):
        """Test that the option ComboBox is present with items."""
        from tests.data.pyside.form_inputs import FormInputs

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(FormInputs, container)

        def check_combobox():
            combo = container.findChild(QtWidgets.QComboBox, "option-combo")
            assert combo is not None
            assert combo.count() == 3

        qtbot.waitUntil(check_combobox, timeout=500)

    def test_form_inputs_font_combobox(self, qapp, qtbot):
        """Test that the FontComboBox is present."""
        from tests.data.pyside.form_inputs import FormInputs

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(FormInputs, container)

        def check_font_combo():
            combo = container.findChild(QtWidgets.QFontComboBox, "font-combo")
            assert combo is not None

        qtbot.waitUntil(check_font_combo, timeout=500)

    def test_form_inputs_date_edit(self, qapp, qtbot):
        """Test that the DateEdit is present."""
        from tests.data.pyside.form_inputs import FormInputs

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(FormInputs, container)

        def check_date_edit():
            date_edit = container.findChild(QtWidgets.QDateEdit, "date-input")
            assert date_edit is not None

        qtbot.waitUntil(check_date_edit, timeout=500)

    def test_form_inputs_time_edit(self, qapp, qtbot):
        """Test that the TimeEdit is present."""
        from tests.data.pyside.form_inputs import FormInputs

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(FormInputs, container)

        def check_time_edit():
            time_edit = container.findChild(QtWidgets.QTimeEdit, "time-input")
            assert time_edit is not None

        qtbot.waitUntil(check_time_edit, timeout=500)

    def test_form_inputs_datetime_edit(self, qapp, qtbot):
        """Test that the DateTimeEdit is present."""
        from tests.data.pyside.form_inputs import FormInputs

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(FormInputs, container)

        def check_datetime_edit():
            dt_edit = container.findChild(QtWidgets.QDateTimeEdit, "datetime-input")
            assert dt_edit is not None

        qtbot.waitUntil(check_datetime_edit, timeout=500)

    def test_form_inputs_key_sequence_edit(self, qapp, qtbot):
        """Test that the KeySequenceEdit is present."""
        from tests.data.pyside.form_inputs import FormInputs

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(FormInputs, container)

        def check_key_seq():
            key_edit = container.findChild(QtWidgets.QKeySequenceEdit, "shortcut-input")
            assert key_edit is not None

        qtbot.waitUntil(check_key_seq, timeout=500)

    def test_form_inputs_summary_label(self, qapp, qtbot):
        """Test that the summary label reflects initial state."""
        from tests.data.pyside.form_inputs import FormInputs

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(FormInputs, container)

        def check_summary():
            label = container.findChild(QtWidgets.QLabel, "summary-label")
            assert label is not None
            assert "Age: 25" in label.text()
            assert "Height: 1.75m" in label.text()

        qtbot.waitUntil(check_summary, timeout=500)


# ---------------------------------------------------------------------------
# Button Types
# ---------------------------------------------------------------------------


class TestButtonTypes:
    def test_button_types_render(self, qapp, qtbot):
        """Test that all button type groups are created."""
        from tests.data.pyside.button_types import ButtonTypes

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(ButtonTypes, container)

        def check_groups():
            push_group = container.findChild(QtWidgets.QGroupBox, "push-group")
            assert push_group is not None
            tool_group = container.findChild(QtWidgets.QGroupBox, "tool-group")
            assert tool_group is not None
            command_group = container.findChild(QtWidgets.QGroupBox, "command-group")
            assert command_group is not None
            radio_group = container.findChild(QtWidgets.QGroupBox, "radio-group")
            assert radio_group is not None
            check_grp = container.findChild(QtWidgets.QGroupBox, "check-group")
            assert check_grp is not None

        qtbot.waitUntil(check_groups, timeout=500)

    def test_push_buttons(self, qapp, qtbot):
        """Test that push button variants are present."""
        from tests.data.pyside.button_types import ButtonTypes

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(ButtonTypes, container)

        def check_buttons():
            normal = container.findChild(QtWidgets.QPushButton, "normal-btn")
            assert normal is not None
            flat = container.findChild(QtWidgets.QPushButton, "flat-btn")
            assert flat is not None
            assert flat.isFlat()
            disabled = container.findChild(QtWidgets.QPushButton, "disabled-btn")
            assert disabled is not None
            assert not disabled.isEnabled()
            checkable = container.findChild(QtWidgets.QPushButton, "checkable-btn")
            assert checkable is not None
            assert checkable.isCheckable()

        qtbot.waitUntil(check_buttons, timeout=500)

    def test_tool_buttons(self, qapp, qtbot):
        """Test that tool buttons are present."""
        from tests.data.pyside.button_types import ButtonTypes

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(ButtonTypes, container)

        def check_tool_buttons():
            tool1 = container.findChild(QtWidgets.QToolButton, "tool-btn-1")
            assert tool1 is not None
            tool2 = container.findChild(QtWidgets.QToolButton, "tool-btn-2")
            assert tool2 is not None
            assert tool2.isCheckable()

        qtbot.waitUntil(check_tool_buttons, timeout=500)

    def test_command_link_button(self, qapp, qtbot):
        """Test that the command link button is present."""
        from tests.data.pyside.button_types import ButtonTypes

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(ButtonTypes, container)

        def check_command_link():
            btn = container.findChild(QtWidgets.QCommandLinkButton, "command-link-btn")
            assert btn is not None
            assert btn.text() == "Command Link"

        qtbot.waitUntil(check_command_link, timeout=500)

    def test_radio_buttons(self, qapp, qtbot):
        """Test that radio buttons are present."""
        from tests.data.pyside.button_types import ButtonTypes

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(ButtonTypes, container)

        def check_radios():
            for i in range(1, 4):
                radio = container.findChild(QtWidgets.QRadioButton, f"radio-{i}")
                assert radio is not None

        qtbot.waitUntil(check_radios, timeout=500)

    def test_checkboxes(self, qapp, qtbot):
        """Test that checkboxes are present, including tri-state."""
        from tests.data.pyside.button_types import ButtonTypes

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(ButtonTypes, container)

        def check_checkboxes():
            check_a = container.findChild(QtWidgets.QCheckBox, "check-a")
            assert check_a is not None
            check_b = container.findChild(QtWidgets.QCheckBox, "check-b")
            assert check_b is not None
            assert check_b.isTristate()

        qtbot.waitUntil(check_checkboxes, timeout=500)

    def test_button_click_updates_label(self, qapp, qtbot):
        """Test that clicking a button updates the status label."""
        from tests.data.pyside.button_types import ButtonTypes

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(ButtonTypes, container)

        normal_btn = None

        def find_btn():
            nonlocal normal_btn
            normal_btn = container.findChild(QtWidgets.QPushButton, "normal-btn")
            assert normal_btn is not None

        qtbot.waitUntil(find_btn, timeout=500)
        qtbot.mouseClick(normal_btn, QtCore.Qt.LeftButton)

        def check_label():
            label = container.findChild(QtWidgets.QLabel, "status-label")
            assert label is not None
            assert "button" in label.text()

        qtbot.waitUntil(check_label, timeout=500)


# ---------------------------------------------------------------------------
# Display Widgets
# ---------------------------------------------------------------------------


class TestDisplayWidgets:
    def test_display_widgets_render(self, qapp, qtbot):
        """Test that display widgets are created."""
        from tests.data.pyside.display_widgets import DisplayWidgets

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(DisplayWidgets, container)

        def check_widgets():
            progress = container.findChild(QtWidgets.QProgressBar, "progress-bar")
            assert progress is not None
            assert progress.value() == 50

        qtbot.waitUntil(check_widgets, timeout=500)

    def test_lcd_number(self, qapp, qtbot):
        """Test that QLCDNumber is present and shows correct value."""
        from tests.data.pyside.display_widgets import DisplayWidgets

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(DisplayWidgets, container)

        def check_lcd():
            lcd = container.findChild(QtWidgets.QLCDNumber, "lcd-display")
            assert lcd is not None
            assert lcd.intValue() == 50

        qtbot.waitUntil(check_lcd, timeout=500)

    def test_calendar_widget(self, qapp, qtbot):
        """Test that QCalendarWidget is present."""
        from tests.data.pyside.display_widgets import DisplayWidgets

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(DisplayWidgets, container)

        def check_calendar():
            cal = container.findChild(QtWidgets.QCalendarWidget, "calendar")
            assert cal is not None

        qtbot.waitUntil(check_calendar, timeout=500)

    def test_text_browser(self, qapp, qtbot):
        """Test that QTextBrowser is present with HTML content."""
        from tests.data.pyside.display_widgets import DisplayWidgets

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(DisplayWidgets, container)

        def check_browser():
            browser = container.findChild(QtWidgets.QTextBrowser, "text-browser")
            assert browser is not None

        qtbot.waitUntil(check_browser, timeout=500)

    def test_slider_changes_progress(self, qapp, qtbot):
        """Test that moving the slider updates progress bar and LCD."""
        from tests.data.pyside.display_widgets import DisplayWidgets

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(DisplayWidgets, container)

        slider = None

        def find_slider():
            nonlocal slider
            slider = container.findChild(QtWidgets.QSlider, "value-slider")
            assert slider is not None

        qtbot.waitUntil(find_slider, timeout=500)

        # Change the slider value programmatically
        slider.setValue(75)

        def check_updated():
            progress = container.findChild(QtWidgets.QProgressBar, "progress-bar")
            assert progress is not None
            assert progress.value() == 75
            lcd = container.findChild(QtWidgets.QLCDNumber, "lcd-display")
            assert lcd is not None
            assert lcd.intValue() == 75

        qtbot.waitUntil(check_updated, timeout=500)


# ---------------------------------------------------------------------------
# Text Editors
# ---------------------------------------------------------------------------


class TestTextEditors:
    def test_text_editors_render(self, qapp, qtbot):
        """Test that text editing widgets are created."""
        from tests.data.pyside.text_editors import TextEditors

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(TextEditors, container)

        def check_widgets():
            line = container.findChild(QtWidgets.QLineEdit, "line-input")
            assert line is not None
            rich = container.findChild(QtWidgets.QTextEdit, "rich-editor")
            assert rich is not None
            plain = container.findChild(QtWidgets.QPlainTextEdit, "plain-editor")
            assert plain is not None

        qtbot.waitUntil(check_widgets, timeout=500)

    def test_line_edit_mirror(self, qapp, qtbot):
        """Test that the mirror LineEdit exists and is read-only."""
        from tests.data.pyside.text_editors import TextEditors

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(TextEditors, container)

        def check_mirror():
            mirror = container.findChild(QtWidgets.QLineEdit, "line-mirror")
            assert mirror is not None
            assert mirror.isReadOnly()

        qtbot.waitUntil(check_mirror, timeout=500)

    def test_password_fields(self, qapp, qtbot):
        """Test that password input fields have correct echo mode."""
        from tests.data.pyside.text_editors import TextEditors

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(TextEditors, container)

        def check_password():
            password = container.findChild(QtWidgets.QLineEdit, "password-input")
            assert password is not None
            assert password.echoMode() == QtWidgets.QLineEdit.Password
            confirm = container.findChild(QtWidgets.QLineEdit, "confirm-input")
            assert confirm is not None
            assert confirm.echoMode() == QtWidgets.QLineEdit.PasswordEchoOnEdit

        qtbot.waitUntil(check_password, timeout=500)

    def test_plain_text_edit(self, qapp, qtbot):
        """Test that QPlainTextEdit has initial content."""
        from tests.data.pyside.text_editors import TextEditors

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(TextEditors, container)

        def check_plain():
            plain = container.findChild(QtWidgets.QPlainTextEdit, "plain-editor")
            assert plain is not None
            assert plain.toPlainText() == "Hello World"

        qtbot.waitUntil(check_plain, timeout=500)


# ---------------------------------------------------------------------------
# Item Views
# ---------------------------------------------------------------------------


class TestItemViews:
    def test_item_views_render(self, qapp, qtbot):
        """Test that list, table, and tree views are created."""
        from tests.data.pyside.item_views import ItemViews

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(ItemViews, container)

        def check_views():
            list_view = container.findChild(QtWidgets.QListView, "list-view")
            assert list_view is not None
            table_view = container.findChild(QtWidgets.QTableView, "table-view")
            assert table_view is not None
            tree_view = container.findChild(QtWidgets.QTreeView, "tree-view")
            assert tree_view is not None

        qtbot.waitUntil(check_views, timeout=500)

    def test_list_model_items(self, qapp, qtbot):
        """Test that the list model has the correct initial items."""
        from tests.data.pyside.item_views import ItemViews

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(ItemViews, container)

        def check_list_model():
            list_view = container.findChild(QtWidgets.QListView, "list-view")
            assert list_view is not None
            model = list_view.model()
            assert model is not None
            assert model.rowCount() == 4
            assert model.item(0).text() == "Apple"

        qtbot.waitUntil(check_list_model, timeout=500)

    def test_table_model_items(self, qapp, qtbot):
        """Test that the table model has correct items and headers."""
        from tests.data.pyside.item_views import ItemViews

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(ItemViews, container)

        def check_table_model():
            table_view = container.findChild(QtWidgets.QTableView, "table-view")
            assert table_view is not None
            model = table_view.model()
            assert model is not None
            assert model.rowCount() == 3
            assert model.columnCount() == 3

        qtbot.waitUntil(check_table_model, timeout=500)

    def test_splitter(self, qapp, qtbot):
        """Test that the main splitter exists."""
        from tests.data.pyside.item_views import ItemViews

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(ItemViews, container)

        def check_splitter():
            splitter = container.findChild(QtWidgets.QSplitter, "main-splitter")
            assert splitter is not None

        qtbot.waitUntil(check_splitter, timeout=500)

    def test_add_item(self, qapp, qtbot):
        """Test that clicking add button adds an item to the list."""
        from tests.data.pyside.item_views import ItemViews

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(ItemViews, container)

        add_btn = None

        def find_btn():
            nonlocal add_btn
            add_btn = container.findChild(QtWidgets.QPushButton, "add-btn")
            assert add_btn is not None

        qtbot.waitUntil(find_btn, timeout=500)
        qtbot.mouseClick(add_btn, QtCore.Qt.LeftButton)

        def check_added():
            list_view = container.findChild(QtWidgets.QListView, "list-view")
            model = list_view.model()
            assert model.rowCount() == 5

        qtbot.waitUntil(check_added, timeout=500)


# ---------------------------------------------------------------------------
# Container Widgets
# ---------------------------------------------------------------------------


class TestContainerWidgets:
    def test_container_widgets_render(self, qapp, qtbot):
        """Test that container widgets are created."""
        from tests.data.pyside.container_widgets import ContainerWidgets

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(ContainerWidgets, container)

        def check_containers():
            tab_widget = container.findChild(QtWidgets.QTabWidget, "tab-widget")
            assert tab_widget is not None

        qtbot.waitUntil(check_containers, timeout=500)

    def test_tab_widget_pages(self, qapp, qtbot):
        """Test that the tab widget has the correct number of tabs."""
        from tests.data.pyside.container_widgets import ContainerWidgets

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(ContainerWidgets, container)

        def check_tabs():
            tab_widget = container.findChild(QtWidgets.QTabWidget, "tab-widget")
            assert tab_widget is not None
            assert tab_widget.count() == 3
            assert tab_widget.tabText(0) == "Tab 1"
            assert tab_widget.tabText(1) == "Tab 2"
            assert tab_widget.tabText(2) == "Tab 3"

        qtbot.waitUntil(check_tabs, timeout=500)

    def test_toolbox(self, qapp, qtbot):
        """Test that the QToolBox is present."""
        from tests.data.pyside.container_widgets import ContainerWidgets

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(ContainerWidgets, container)

        def check_toolbox():
            toolbox = container.findChild(QtWidgets.QToolBox, "tool-box")
            assert toolbox is not None

        qtbot.waitUntil(check_toolbox, timeout=500)

    def test_stacked_widget(self, qapp, qtbot):
        """Test that the QStackedWidget is present."""
        from tests.data.pyside.container_widgets import ContainerWidgets

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(ContainerWidgets, container)

        def check_stacked():
            stacked = container.findChild(QtWidgets.QStackedWidget, "stacked-widget")
            assert stacked is not None

        qtbot.waitUntil(check_stacked, timeout=500)

    def test_scroll_area(self, qapp, qtbot):
        """Test that the QScrollArea is present with content."""
        from tests.data.pyside.container_widgets import ContainerWidgets

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(ContainerWidgets, container)

        def check_scroll():
            scroll = container.findChild(QtWidgets.QScrollArea, "scroll-area")
            assert scroll is not None

        qtbot.waitUntil(check_scroll, timeout=500)

    def test_frames(self, qapp, qtbot):
        """Test that QFrame instances are present with correct styles."""
        from tests.data.pyside.container_widgets import ContainerWidgets

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(ContainerWidgets, container)

        def check_frames():
            box_frame = container.findChild(QtWidgets.QFrame, "styled-frame")
            assert box_frame is not None
            assert box_frame.frameShape() == QtWidgets.QFrame.Box
            raised_frame = container.findChild(QtWidgets.QFrame, "raised-frame")
            assert raised_frame is not None
            assert raised_frame.frameShape() == QtWidgets.QFrame.StyledPanel

        qtbot.waitUntil(check_frames, timeout=500)


# ---------------------------------------------------------------------------
# Dialog Widgets
# ---------------------------------------------------------------------------


class TestDialogWidgets:
    def test_dialog_widgets_render(self, qapp, qtbot):
        """Test that the dialog launcher buttons are created."""
        from tests.data.pyside.dialog_widgets import DialogWidgets

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(DialogWidgets, container)

        def check_buttons():
            msgbox_btn = container.findChild(QtWidgets.QPushButton, "msgbox-btn")
            assert msgbox_btn is not None
            input_btn = container.findChild(QtWidgets.QPushButton, "input-btn")
            assert input_btn is not None
            custom_btn = container.findChild(QtWidgets.QPushButton, "custom-btn")
            assert custom_btn is not None
            progress_btn = container.findChild(QtWidgets.QPushButton, "progress-btn")
            assert progress_btn is not None

        qtbot.waitUntil(check_buttons, timeout=500)

    def test_custom_dialog_toggle(self, qapp, qtbot):
        """Test that clicking the custom dialog button shows the dialog."""
        from tests.data.pyside.dialog_widgets import DialogWidgets

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(DialogWidgets, container)

        custom_btn = None

        def find_btn():
            nonlocal custom_btn
            custom_btn = container.findChild(QtWidgets.QPushButton, "custom-btn")
            assert custom_btn is not None

        qtbot.waitUntil(find_btn, timeout=500)

        # No dialog initially
        def no_dialog():
            dialog = container.findChild(QtWidgets.QDialog, "custom-dialog")
            assert dialog is None

        qtbot.waitUntil(no_dialog, timeout=500)

        # Click to show dialog
        qtbot.mouseClick(custom_btn, QtCore.Qt.LeftButton)

        def check_dialog_shown():
            # The dialog is a top-level widget, search app-wide
            dialogs = [
                w for w in qapp.topLevelWidgets() if isinstance(w, QtWidgets.QDialog)
            ]
            assert len(dialogs) >= 1

        qtbot.waitUntil(check_dialog_shown, timeout=500)

    def test_result_label(self, qapp, qtbot):
        """Test that the result label shows initial state."""
        from tests.data.pyside.dialog_widgets import DialogWidgets

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(DialogWidgets, container)

        def check_label():
            label = container.findChild(QtWidgets.QLabel, "result-label")
            assert label is not None
            assert "none" in label.text()

        qtbot.waitUntil(check_label, timeout=500)


# ---------------------------------------------------------------------------
# Slider / Dial Widgets
# ---------------------------------------------------------------------------


class TestSliderDialWidgets:
    def test_slider_dial_render(self, qapp, qtbot):
        """Test that slider, dial, and scrollbar widgets are created."""
        from tests.data.pyside.slider_dial_widgets import SliderDialWidgets

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(SliderDialWidgets, container)

        def check_widgets():
            h_slider = container.findChild(QtWidgets.QSlider, "h-slider")
            assert h_slider is not None
            assert h_slider.orientation() == QtCore.Qt.Horizontal
            v_slider = container.findChild(QtWidgets.QSlider, "v-slider")
            assert v_slider is not None
            assert v_slider.orientation() == QtCore.Qt.Vertical
            dial = container.findChild(QtWidgets.QDial, "dial")
            assert dial is not None
            assert dial.notchesVisible()
            scrollbar = container.findChild(QtWidgets.QScrollBar, "scrollbar")
            assert scrollbar is not None

        qtbot.waitUntil(check_widgets, timeout=500)

    def test_initial_values(self, qapp, qtbot):
        """Test that all controls show initial value of 50."""
        from tests.data.pyside.slider_dial_widgets import SliderDialWidgets

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(SliderDialWidgets, container)

        def check_values():
            h_slider = container.findChild(QtWidgets.QSlider, "h-slider")
            assert h_slider.value() == 50
            dial = container.findChild(QtWidgets.QDial, "dial")
            assert dial.value() == 50
            lcd = container.findChild(QtWidgets.QLCDNumber, "lcd")
            assert lcd.intValue() == 50
            progress = container.findChild(QtWidgets.QProgressBar, "progress")
            assert progress.value() == 50
            label = container.findChild(QtWidgets.QLabel, "value-label")
            assert "50" in label.text()

        qtbot.waitUntil(check_values, timeout=500)

    def test_slider_change_propagates(self, qapp, qtbot):
        """Test that changing the slider updates other displays."""
        from tests.data.pyside.slider_dial_widgets import SliderDialWidgets

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(SliderDialWidgets, container)

        slider = None

        def find_slider():
            nonlocal slider
            slider = container.findChild(QtWidgets.QSlider, "h-slider")
            assert slider is not None

        qtbot.waitUntil(find_slider, timeout=500)

        slider.setValue(80)

        def check_propagated():
            lcd = container.findChild(QtWidgets.QLCDNumber, "lcd")
            assert lcd.intValue() == 80
            progress = container.findChild(QtWidgets.QProgressBar, "progress")
            assert progress.value() == 80
            label = container.findChild(QtWidgets.QLabel, "value-label")
            assert "80" in label.text()

        qtbot.waitUntil(check_propagated, timeout=500)


# ---------------------------------------------------------------------------
# MDI Area
# ---------------------------------------------------------------------------


class TestMdiArea:
    def test_mdi_area_render(self, qapp, qtbot):
        """Test that the MDI window with subwindows is created."""
        from tests.data.pyside.mdi_area import MdiArea

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        gui.render(MdiArea, qapp)

        window = None

        def check_window():
            nonlocal window
            window = get_current_window(qapp)
            assert window is not None

        qtbot.waitUntil(check_window, timeout=500)

        def check_mdi():
            mdi = window.findChild(QtWidgets.QMdiArea, "mdi-area")
            assert mdi is not None

        qtbot.waitUntil(check_mdi, timeout=500)

    def test_mdi_subwindows(self, qapp, qtbot):
        """Test that initial subwindows are present."""
        from tests.data.pyside.mdi_area import MdiArea

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        gui.render(MdiArea, qapp)

        window = None

        def check_window():
            nonlocal window
            window = get_current_window(qapp)
            assert window is not None

        qtbot.waitUntil(check_window, timeout=500)

        def check_subwindows():
            sub0 = window.findChild(QtWidgets.QMdiSubWindow, "subwindow-0")
            assert sub0 is not None
            sub1 = window.findChild(QtWidgets.QMdiSubWindow, "subwindow-1")
            assert sub1 is not None

        qtbot.waitUntil(check_subwindows, timeout=500)

    def test_mdi_menu_actions(self, qapp, qtbot):
        """Test that MDI window menu actions are present."""
        from tests.data.pyside.mdi_area import MdiArea

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        gui.render(MdiArea, qapp)

        window = None

        def check_window():
            nonlocal window
            window = get_current_window(qapp)
            assert window is not None

        qtbot.waitUntil(check_window, timeout=500)

        def check_actions():
            new_action = window.findChild(QtGui.QAction, "new-window-action")
            assert new_action is not None
            cascade_action = window.findChild(QtGui.QAction, "cascade-action")
            assert cascade_action is not None
            tile_action = window.findChild(QtGui.QAction, "tile-action")
            assert tile_action is not None

        qtbot.waitUntil(check_actions, timeout=500)

    def test_mdi_statusbar(self, qapp, qtbot):
        """Test that the MDI window has a statusbar."""
        from tests.data.pyside.mdi_area import MdiArea

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        gui.render(MdiArea, qapp)

        window = None

        def check_window():
            nonlocal window
            window = get_current_window(qapp)
            assert window is not None

        qtbot.waitUntil(check_window, timeout=500)

        def check_statusbar():
            statusbar = window.findChild(QtWidgets.QStatusBar, "mdi-statusbar")
            assert statusbar is not None

        qtbot.waitUntil(check_statusbar, timeout=500)


# ---------------------------------------------------------------------------
# Wizard Widget
# ---------------------------------------------------------------------------


class TestWizardWidget:
    def test_wizard_widget_render(self, qapp, qtbot):
        """Test that the wizard launcher is created."""
        from tests.data.pyside.wizard_widget import WizardWidget

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(WizardWidget, container)

        def check_launch_btn():
            btn = container.findChild(QtWidgets.QPushButton, "launch-btn")
            assert btn is not None

        qtbot.waitUntil(check_launch_btn, timeout=500)

    def test_wizard_initial_state(self, qapp, qtbot):
        """Test that the wizard is not shown initially."""
        from tests.data.pyside.wizard_widget import WizardWidget

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(WizardWidget, container)

        def check_no_wizard():
            label = container.findChild(QtWidgets.QLabel, "result-label")
            assert label is not None
            assert "not started" in label.text()

        qtbot.waitUntil(check_no_wizard, timeout=500)

    def test_wizard_launch(self, qapp, qtbot):
        """Test that clicking launch shows the wizard."""
        from tests.data.pyside.wizard_widget import WizardWidget

        renderer = cg.PySideRenderer(autoshow=False)
        gui = cg.Collagraph(renderer=renderer)
        container = renderer.create_element("widget")
        gui.render(WizardWidget, container)

        launch_btn = None

        def find_btn():
            nonlocal launch_btn
            launch_btn = container.findChild(QtWidgets.QPushButton, "launch-btn")
            assert launch_btn is not None

        qtbot.waitUntil(find_btn, timeout=500)
        qtbot.mouseClick(launch_btn, QtCore.Qt.LeftButton)

        def check_wizard_shown():
            label = container.findChild(QtWidgets.QLabel, "result-label")
            assert label is not None
            assert "in progress" in label.text()

        qtbot.waitUntil(check_wizard_shown, timeout=500)
