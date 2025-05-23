import textwrap


LOGO_TEMPLATE_MOD = textwrap.dedent("""\
<table width="100%" style="table-layout: fixed; border: none;">
    <colgroup>
        <col style="width: 50%;" />
        <col style="width: 50%;" />
    </colgroup>
    <tr>
        <td style="text-align: left;">
            <img height="80" src="{}" />
        </td>
        <td style="text-align: right;">
            <img height="80" src="{}" />
        </td>
    </tr>
</table>
<br>

""")


LOGO_TEMPLATE = textwrap.dedent("""\
<p>
    <img src="{}" style="float: left; height: 80px; display: block;" />
    <img src="{}" style="float: right; height: 80px; display: block;" />
</p>
<br clear="both">
<br>

""")