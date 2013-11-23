<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="http://www.w3.org/1999/xhtml">

    <xsl:template match="food" mode="food_menu">
        <h3><xsl:value-of select="name"/></h3>
        <xsl:call-template name="price-label"/><br/>
        <xsl:apply-templates select="." mode="description"/><br/>
        <xsl:apply-templates select="." mode="calories"/>
    </xsl:template>

    <xsl:template name="price-label">
        <span style="color: gray;"><xsl:value-of select="price"/></span>
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
