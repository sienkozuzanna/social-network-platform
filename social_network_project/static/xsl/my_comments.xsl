<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="html" indent="yes"/>
    <xsl:template match="/">
        <html>
            <head>
                <title>User Comments</title>
                <style>
                    body { font-family: sans-serif; margin: 20px; }
                    table { width: 100%; border-collapse: collapse; }
                    th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
                    th { font-weight: bold; }
                    tr:hover { background-color: #f9f9f9; }
                </style>
            </head>
            <body>
                <h1>User Comments</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Content</th>
                            <th>Post ID</th>
                            <th>Created At</th>
                        </tr>
                    </thead>
                    <tbody>
                        <xsl:for-each select="comments/comment">
                            <tr>
                                <td><xsl:value-of select="content"/></td>
                                <td><xsl:value-of select="post_id"/></td>
                                <td><xsl:value-of select="created_at"/></td>
                            </tr>
                        </xsl:for-each>
                    </tbody>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
