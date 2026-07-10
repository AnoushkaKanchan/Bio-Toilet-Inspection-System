import pytest

from apps.ntes.dto import RawCoachDTO
from apps.ntes.exceptions import NTESParsingError
from apps.ntes.parser import NTESHTMLParser


@pytest.fixture
def parser():
    return NTESHTMLParser()


def test_parse_single_coach(parser):
    html = """
    <table>
        <tbody>
            <tr>
                <td>
                    <div style="display:inline-block;width:45px;height:60px;">
                        <div>GS</div>
                        <div><b>223456</b></div>
                        <div>1</div>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
    """

    result = parser.parse(html)

    assert result == [
        RawCoachDTO(
            coach_sequence="1",
            coach_number="223456",
            coach_type="GS",
        )
    ]


def test_parse_multiple_coaches(parser):
    html = """
    <table>
        <tbody>
            <tr>
                <td>

                    <div style="display:inline-block;">
                        <div>GS</div>
                        <div><b>111111</b></div>
                        <div>1</div>
                    </div>

                    <div style="display:inline-block;">
                        <div>SLR</div>
                        <div><b>222222</b></div>
                        <div>2</div>
                    </div>

                </td>
            </tr>
        </tbody>
    </table>
    """

    result = parser.parse(html)

    assert len(result) == 2

    assert result[0].coach_type == "GS"
    assert result[1].coach_type == "SLR"


def test_empty_html(parser):
    with pytest.raises(NTESParsingError):
        parser.parse("")


def test_invalid_structure(parser):
    with pytest.raises(NTESParsingError):
        parser.parse("<html></html>")


def test_missing_b_tag_skips_block(parser):
    html = """
    <table>
        <tbody>
            <tr>
                <td>

                    <div style="display:inline-block;">
                        <div>GS</div>
                        <div>223456</div>
                        <div>1</div>
                    </div>

                </td>
            </tr>
        </tbody>
    </table>
    """

    result = parser.parse(html)

    assert result == []


def test_raw_values_preserved(parser):
    html = """
    <table>
        <tbody>
            <tr>
                <td>

                    <div style="display:inline-block;">
                        <div> GS </div>
                        <div><b> B3 </b></div>
                        <div> 01 </div>
                    </div>

                </td>
            </tr>
        </tbody>
    </table>
    """

    result = parser.parse(html)

    assert result[0].coach_type == " GS "
    assert result[0].coach_number == " B3 "
    assert result[0].coach_sequence == " 01 "
