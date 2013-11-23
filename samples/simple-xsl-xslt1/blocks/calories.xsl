<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="http://www.w3.org/1999/xhtml">

    <xsl:import href="description-tag.xsl"/>

    <xsl:template match="food[key('calories', @key) >= 650]" mode="calories">
        <xsl:message><xsl:value-of select="@key" />650</xsl:message>
        <xsl:call-template name="calories-label">
            <xsl:with-param name="color" select="'orange'"/>
        </xsl:call-template>
    </xsl:template>

    <xsl:template match="food[key('calories', @key) >= 800]" mode="calories">
        <xsl:message>850</xsl:message>
        <xsl:call-template name="calories-label">
            <xsl:with-param name="color" select="'red'"/>
        </xsl:call-template>
    </xsl:template>

    <xsl:template name="calories-label">
        <xsl:param name="color"/>
        <span>
            <xsl:attribute name="style">color: <xsl:value-of select="$color"/>;</xsl:attribute>
            <xsl:value-of select="key('calories', @key)"/>
        </span><br/>
    </xsl:template>

    <xsl:template match="food" mode="calories"><xsl:message>default</xsl:message></xsl:template>

    <xsl:output omit-xml-declaration="yes"
                method="xml"
                indent="yes"
                encoding="UTF-8"
                media-type="text/html;"
                doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"
                doctype-public="-//W3C//DTD XHTML 1.1//EN"
                version="1.1"/>
</xsl:stylesheet>
