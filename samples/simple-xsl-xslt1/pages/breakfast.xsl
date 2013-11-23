<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="http://www.w3.org/1999/xhtml">

    <xsl:import href="../blocks/item.xsl"/>
    <xsl:import href="../blocks/description.xsl"/>
    <xsl:import href="../blocks/calories.xsl"/>

    <xsl:key name="calories" match="/breakfastMenu/calories/item" use="@key"/>

    <xsl:template match="/breakfastMenu">
        <html>
            <body>
                <h1>Breakfast</h1>
                <xsl:apply-templates select="food" mode="food_menu"/>
            </body>
        </html>
    </xsl:template>

    <xsl:output omit-xml-declaration="yes"
                method="xml"
                indent="yes"
                encoding="UTF-8"
                media-type="text/html;"
                doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"
                doctype-public="-//W3C//DTD XHTML 1.1//EN"
                version="1.1"/>
</xsl:stylesheet>
