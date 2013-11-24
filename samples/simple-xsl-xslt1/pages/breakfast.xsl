<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="http://www.w3.org/1999/xhtml">

    <xsl:import href="../blocks/item.xsl"/>
    <xsl:import href="../blocks/description.xsl"/>
    <xsl:import href="../blocks/calories.xsl"/>

    <xsl:key name="calories" match="/breakfastMenu/calories/item" use="@key"/>

    <xsl:template match="/breakfastMenu">
        <xsl:message>
            <xsl:apply-templates mode="path" select="."/>
        </xsl:message>
        <html>
            <body>
                <h1>Breakfast</h1>
                <xsl:apply-templates select="food" mode="food_menu"/>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="*" mode="path">
        <xsl:value-of select="concat('/',name())"/>
        <xsl:variable name="vnumPrecSiblings" select=
        "count(preceding-sibling::*[name()=name(current())])"/>
        <xsl:variable name="vnumFollSiblings" select=
        "count(following-sibling::*[name()=name(current())])"/>
        <xsl:if test="$vnumPrecSiblings or $vnumFollSiblings">
            <xsl:value-of select=
            "concat('[', $vnumPrecSiblings +1, ']')"/>
        </xsl:if>
    </xsl:template>

    <xsl:template match="@*" mode="path">
     <xsl:apply-templates select="ancestor::*" mode="path"/>
     <xsl:value-of select="concat('/@', name())"/>
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
