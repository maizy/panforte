<xsl:template match="*" mode="panforte-path">
    <xsl:value-of select="concat('/',name())"/>
    <xsl:variable name="vnumPrecSiblings"
                  select="count(preceding-sibling::*[name()=name(current())])"/>
    <xsl:variable name="vnumFollSiblings"
                  select="count(following-sibling::*[name()=name(current())])"/>
    <xsl:if test="$vnumPrecSiblings or $vnumFollSiblings">
        <xsl:value-of select="concat('[', $vnumPrecSiblings +1, ']')"/>
    </xsl:if>
</xsl:template>

<xsl:template match="@*" mode="panforte-path">
    <xsl:apply-templates select="ancestor::*" mode="panforte-path"/>
    <xsl:value-of select="concat('/@', name())"/>
</xsl:template>
