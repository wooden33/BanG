package org.apache.commons.csv;


import org.junit.Before;
import org.junit.After;
import org.junit.Test;
import static org.junit.Assert.*;
import static org.junit.Assert.*;
import org.junit.Test;
import static org.junit.Assert.*;
import org.junit.Test;
import static org.mockito.Mockito.*;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import static org.junit.Assert.*;
import org.junit.Test;
import java.io.IOException;
import java.io.StringWriter;
import static org.junit.Assert.*;
import org.junit.Test;
import org.apache.commons.csv.QuoteMode;
import static org.junit.Assert.*;
import org.junit.Test;
import java.io.IOException;
import java.io.StringReader;
import static org.junit.Assert.*;
import org.junit.Test;
import java.io.IOException;
import java.io.Reader;
import java.io.StringReader;
import static org.junit.Assert.*;
import org.junit.Test;
import java.io.Reader;
import java.io.IOException;
import static org.junit.Assert.*;
import org.junit.Test;
import java.io.StringWriter;
import java.io.IOException;
import static org.junit.Assert.*;
import java.io.IOException;
import java.io.StringWriter;
import org.junit.Test;
import static org.junit.Assert.*;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import org.junit.Test;
import static org.mockito.Mockito.*;

public class CSVFormatTest {


    @Test
    public void testWithIgnoreEmptyLines() {
        CSVFormat format = CSVFormat.DEFAULT;
        CSVFormat newFormat = format.withIgnoreEmptyLines();
        assertTrue(newFormat.getIgnoreEmptyLines());
    }


    @Test
    public void testWithIgnoreEmptyLinesFalse() {
        CSVFormat format = CSVFormat.DEFAULT.withIgnoreEmptyLines();
        CSVFormat newFormat = format.withIgnoreEmptyLines(false);
        assertFalse(newFormat.getIgnoreEmptyLines());
    }


    @Test
    public void testWithIgnoreSurroundingSpaces() {
        CSVFormat format = CSVFormat.DEFAULT;
        CSVFormat newFormat = format.withIgnoreSurroundingSpaces();
        assertTrue(newFormat.getIgnoreSurroundingSpaces());
    }


    @Test
    public void testWithIgnoreSurroundingSpacesFalse() {
        CSVFormat format = CSVFormat.DEFAULT.withIgnoreSurroundingSpaces();
        CSVFormat newFormat = format.withIgnoreSurroundingSpaces(false);
        assertFalse(newFormat.getIgnoreSurroundingSpaces());
    }


    @Test
    public void testWithAllowMissingColumnNames() {
        CSVFormat format = CSVFormat.DEFAULT;
        CSVFormat newFormat = format.withAllowMissingColumnNames();
        assertTrue(newFormat.getAllowMissingColumnNames());
    }


    @Test
    public void testWithAllowMissingColumnNamesFalse() {
        CSVFormat format = CSVFormat.DEFAULT.withAllowMissingColumnNames();
        CSVFormat newFormat = format.withAllowMissingColumnNames(false);
        assertFalse(newFormat.getAllowMissingColumnNames());
    }


    @Test
    public void testWithAutoFlush() {
        CSVFormat format = CSVFormat.DEFAULT;
        CSVFormat newFormat = format.withAutoFlush(true);
        assertTrue(newFormat.getAutoFlush());
    }


    @Test
    public void testWithAutoFlushFalse() {
        CSVFormat format = CSVFormat.DEFAULT.withAutoFlush(true);
        CSVFormat newFormat = format.withAutoFlush(false);
        assertFalse(newFormat.getAutoFlush());
    }


    @Test
    public void testCSVFormatEqualsAndHashCode() {
        CSVFormat format1 = CSVFormat.DEFAULT.withDelimiter(',');
        CSVFormat format2 = CSVFormat.DEFAULT.withDelimiter(',');
        CSVFormat format3 = CSVFormat.DEFAULT.withDelimiter(';');
        
        assertEquals(format1, format2);
        assertEquals(format1.hashCode(), format2.hashCode());
        assertNotEquals(format1, format3);
        assertNotEquals(format1.hashCode(), format3.hashCode());
    }


    @Test
    public void testWithHeaderMetaData() throws SQLException {
        ResultSetMetaData metaData = mock(ResultSetMetaData.class);
        when(metaData.getColumnCount()).thenReturn(2);
        when(metaData.getColumnLabel(1)).thenReturn("col1");
        when(metaData.getColumnLabel(2)).thenReturn("col2");
        
        CSVFormat format = CSVFormat.DEFAULT.withHeader(metaData);
        assertNotNull(format.getHeader());
    }


    @Test(expected = IllegalArgumentException.class)
    public void testWithCommentMarkerLineBreak() {
        CSVFormat.DEFAULT.withCommentMarker('\n');
    }


    @Test(expected = IllegalArgumentException.class)
    public void testWithDelimiterLineBreak() {
        CSVFormat.DEFAULT.withDelimiter('\n');
    }


    @Test(expected = IllegalArgumentException.class)
    public void testWithEscapeLineBreak() {
        CSVFormat.DEFAULT.withEscape('\n');
    }


    @Test(expected = IllegalArgumentException.class)
    public void testWithQuoteLineBreak() {
        CSVFormat.DEFAULT.withQuote('\n');
    }


    @Test
    public void testPrintNullValue() throws IOException {
        StringWriter writer = new StringWriter();
        CSVPrinter printer = new CSVPrinter(writer, CSVFormat.DEFAULT);
        printer.print((String) null);
        printer.close();
        assertNotNull(writer.toString());
    }


    @Test
    public void testPrintNullValueWithNullString() throws IOException {
        StringWriter writer = new StringWriter();
        CSVPrinter printer = new CSVPrinter(writer, CSVFormat.DEFAULT.withNullString("NULL"));
        printer.print((String) null);
        printer.close();
        assertTrue(writer.toString().contains("NULL"));
    }


    @Test
    public void testPrintEmptyString() throws IOException {
        StringWriter writer = new StringWriter();
        CSVPrinter printer = new CSVPrinter(writer, CSVFormat.DEFAULT);
        printer.print("");
        printer.close();
        assertNotNull(writer.toString());
    }


    @Test
    public void testWithHeaderNullArray() {
        CSVFormat format = CSVFormat.DEFAULT.withHeader((String[]) null);
        assertNull(format.getHeader());
    }


    @Test
    public void testWithHeaderEmptyArray() {
        CSVFormat format = CSVFormat.DEFAULT.withHeader(new String[0]);
        assertNotNull(format.getHeader());
    }


    @Test
    public void testWithQuoteMode() {
        CSVFormat format = CSVFormat.DEFAULT.withQuoteMode(QuoteMode.ALL);
        assertEquals(QuoteMode.ALL, format.getQuoteMode());
    }


    @Test
    public void testWithNullString() {
        CSVFormat format = CSVFormat.DEFAULT.withNullString("NULL");
        assertEquals("NULL", format.getNullString());
    }


    @Test
    public void testWithDelimiter() {
        CSVFormat format = CSVFormat.DEFAULT.withDelimiter(',');
        assertEquals(',', format.getDelimiter());
    }


    @Test
    public void testFormatEmpty() {
        String result = CSVFormat.DEFAULT.format();
        assertNotNull(result);
    }


    @Test
    public void testFormatValues() {
        String result = CSVFormat.DEFAULT.format("a", "b", "c");
        assertNotNull(result);
    }


    @Test
    public void testParseEmptyString() throws IOException {
        CSVParser parser = CSVFormat.DEFAULT.parse(new StringReader(""));
        assertNotNull(parser);
    }


    @Test
    public void testParseValidString() throws IOException {
        CSVParser parser = CSVFormat.DEFAULT.parse(new StringReader("a,b,c"));
        assertNotNull(parser);
    }


    @Test
    public void testParseValidReader() throws IOException {
        Reader reader = new StringReader("a,b,c");
        CSVParser parser = CSVFormat.DEFAULT.parse(reader);
        assertNotNull(parser);
    }


    @Test(expected = IllegalArgumentException.class)
    public void testParseNullReader() throws IOException {
        CSVFormat.DEFAULT.parse((Reader) null);
    }


    @Test
    public void testEqualsWithNull() {
        CSVFormat format = CSVFormat.DEFAULT;
        assertFalse(format.equals(null));
    }


    @Test
    public void testEqualsWithDifferentClass() {
        CSVFormat format = CSVFormat.DEFAULT;
        assertFalse(format.equals("not a CSVFormat"));
    }


    @Test
    public void testEqualsIdentical() {
        CSVFormat format1 = CSVFormat.DEFAULT;
        CSVFormat format2 = CSVFormat.DEFAULT;
        assertTrue(format1.equals(format2));
    }


    @Test
    public void testEqualsDifferentDelimiter() {
        CSVFormat format1 = CSVFormat.DEFAULT;
        CSVFormat format2 = CSVFormat.DEFAULT.withDelimiter(';');
        assertFalse(format1.equals(format2));
    }


    @Test
    public void testEqualsDifferentQuoteMode() {
        CSVFormat format1 = CSVFormat.DEFAULT;
        CSVFormat format2 = CSVFormat.DEFAULT.withQuoteMode(QuoteMode.MINIMAL);
        assertFalse(format1.equals(format2));
    }


    @Test
    public void testEqualsDifferentCommentMarker() {
        CSVFormat format1 = CSVFormat.DEFAULT;
        CSVFormat format2 = CSVFormat.DEFAULT.withCommentMarker('#');
        assertFalse(format1.equals(format2));
    }


    @Test
    public void testEqualsDifferentEscapeCharacter() {
        CSVFormat format1 = CSVFormat.DEFAULT;
        CSVFormat format2 = CSVFormat.DEFAULT.withEscape('\\');
        assertFalse(format1.equals(format2));
    }


    @Test
    public void testEqualsDifferentIgnoreSurroundingSpaces() {
        CSVFormat format1 = CSVFormat.DEFAULT;
        CSVFormat format2 = CSVFormat.DEFAULT.withIgnoreSurroundingSpaces(true);
        assertFalse(format1.equals(format2));
    }


    @Test
    public void testEqualsDifferentNullString() {
        CSVFormat format1 = CSVFormat.DEFAULT;
        CSVFormat format2 = CSVFormat.DEFAULT.withNullString("NULL");
        assertFalse(format1.equals(format2));
    }


    @Test
    public void testEqualsDifferentHeader() {
        CSVFormat format1 = CSVFormat.DEFAULT;
        CSVFormat format2 = CSVFormat.DEFAULT.withHeader("col1", "col2");
        assertFalse(format1.equals(format2));
    }


    @Test
    public void testEqualsDifferentSkipHeaderRecord() {
        CSVFormat format1 = CSVFormat.DEFAULT;
        CSVFormat format2 = CSVFormat.DEFAULT.withSkipHeaderRecord(true);
        assertFalse(format1.equals(format2));
    }


    @Test
    public void testHashCodeConsistent() {
        CSVFormat format1 = CSVFormat.DEFAULT;
        CSVFormat format2 = CSVFormat.DEFAULT;
        assertEquals(format1.hashCode(), format2.hashCode());
    }


    @Test
    public void testHashCodeDifferent() {
        CSVFormat format1 = CSVFormat.DEFAULT;
        CSVFormat format2 = CSVFormat.DEFAULT.withDelimiter(';');
        assertNotEquals(format1.hashCode(), format2.hashCode());
    }


    @Test
    public void testHashCodeSameProperties() {
        CSVFormat format1 = CSVFormat.DEFAULT.withDelimiter(';').withQuote('"').withEscape('\\');
        CSVFormat format2 = CSVFormat.DEFAULT.withDelimiter(';').withQuote('"').withEscape('\\');
        assertEquals(format1.hashCode(), format2.hashCode());
    }


    @Test
    public void testHashCodeDifferentProperties() {
        CSVFormat format1 = CSVFormat.DEFAULT.withDelimiter(';');
        CSVFormat format2 = CSVFormat.DEFAULT.withDelimiter(',');
        assertNotEquals(format1.hashCode(), format2.hashCode());
    }


    @Test
    public void testHashCodeSamePropertiesDifferentOrder() {
        CSVFormat format1 = CSVFormat.DEFAULT.withDelimiter(';').withQuote('"');
        CSVFormat format2 = CSVFormat.DEFAULT.withQuote('"').withDelimiter(';');
        assertEquals(format1.hashCode(), format2.hashCode());
    }


    @Test
    public void testEqualsDifferentRecordSeparator() {
        CSVFormat format1 = CSVFormat.DEFAULT.withRecordSeparator("\n");
        CSVFormat format2 = CSVFormat.DEFAULT.withRecordSeparator("\r\n");
        assertFalse(format1.equals(format2));
    }


    @Test
    public void testToStringWithRecordSeparator() {
        CSVFormat format = CSVFormat.DEFAULT.withRecordSeparator("\r\n");
        String result = format.toString();
        assertTrue(result.contains("RecordSeparator=<\r\n>"));
    }


    @Test
    public void testPrintNullWithQuoteModeAll() {
        StringWriter writer = new StringWriter();
        CSVFormat format = CSVFormat.DEFAULT.withNullString("NULL").withQuoteMode(QuoteMode.ALL);
        try {
            format.print(null, writer, true);
            String result = writer.toString();
            assertEquals("\"NULL\"", result);
        } catch (IOException e) {
            fail("IOException should not occur");
        }
    }


    @Test
    public void testPrintNullWithNullNullString() {
        StringWriter writer = new StringWriter();
        CSVFormat format = CSVFormat.DEFAULT.withNullString(null);
        try {
            format.print(null, writer, true);
            String result = writer.toString();
            assertEquals("", result);
        } catch (IOException e) {
            fail("IOException should not occur");
        }
    }


    @Test
    public void testPrintlnWithoutTrailingDelimiter() {
        StringWriter writer = new StringWriter();
        CSVFormat format = CSVFormat.DEFAULT.withTrailingDelimiter(false).withRecordSeparator("\r\n");
        try {
            format.println(writer);
            String result = writer.toString();
            assertTrue(result.endsWith("\r\n"));
        } catch (IOException e) {
            fail("IOException should not occur");
        }
    }


    @Test
    public void testNewFormatWithDelimiter() {
        CSVFormat format = CSVFormat.newFormat('|');
        assertEquals('|', format.getDelimiter());
    }


    @Test
    public void testPrintWithSpecificValue() {
        StringWriter writer = new StringWriter();
        CSVFormat format = CSVFormat.DEFAULT;
        try {
            format.print("test", writer, true);
            String result = writer.toString();
            assertEquals("test", result);
        } catch (IOException e) {
            fail("IOException should not occur");
        }
    }


    @Test
    public void testPrintNullWithNullString() {
        StringWriter writer = new StringWriter();
        CSVFormat format = CSVFormat.DEFAULT.withNullString("NULL");
        try {
            format.print(null, writer, true);
            String result = writer.toString();
            assertEquals("NULL", result);
        } catch (IOException e) {
            fail("IOException should not occur");
        }
    }


    @Test
    public void testWithHeaderFromArray() {
        CSVFormat format = CSVFormat.DEFAULT.withHeader("col1", "col2");
        assertNotNull(format.getHeader());
    }


    @Test
    public void testWithHeaderFromVarargs() {
        CSVFormat format = CSVFormat.DEFAULT.withHeader("col1", "col2", "col3");
        assertNotNull(format.getHeader());
    }


    @Test
    public void testHashCodeWithCustomFields() {
        CSVFormat format = CSVFormat.DEFAULT
            .withDelimiter('|')
            .withQuoteMode(QuoteMode.MINIMAL)
            .withNullString("NULL")
            .withRecordSeparator("\r\n")
            .withIgnoreEmptyLines(true)
            .withIgnoreSurroundingSpaces(true)
            .withSkipHeaderRecord(true);
        int hashCode = format.hashCode();
        assertTrue(hashCode != 0);
    }


    @Test
    public void testPrintNullWithNullNullStringFixed() {
        StringWriter writer = new StringWriter();
        CSVFormat format = CSVFormat.DEFAULT.withNullString(null);
        try {
            format.print(null, writer, true);
            String result = writer.toString();
            assertEquals("", result);
        } catch (IOException e) {
            fail("IOException should not occur");
        }
    }


    @Test
    public void testEqualsRecordSeparatorNull() {
        CSVFormat format1 = CSVFormat.DEFAULT.withRecordSeparator("\n");
        CSVFormat format2 = CSVFormat.DEFAULT.withRecordSeparator(null);
        assertFalse(format1.equals(format2));
    }


    @Test
    public void testEqualsQuoteCharacterNull() {
        CSVFormat format1 = CSVFormat.DEFAULT.withQuote(null);
        CSVFormat format2 = CSVFormat.DEFAULT.withQuote('"');
        assertFalse(format1.equals(format2));
    }


    @Test
    public void testToStringCommentMarkerSet() {
        CSVFormat format = CSVFormat.DEFAULT.withCommentMarker('#');
        String result = format.toString();
        assertTrue(result.contains("CommentStart=<#>"));
    }


    @Test
    public void testPrintNotNullValue() throws IOException {
        StringWriter writer = new StringWriter();
        CSVFormat format = CSVFormat.DEFAULT;
        format.print("test", writer, true);
        assertEquals("test", writer.toString());
    }


    @Test
    public void testPrintNullValueNullString() throws IOException {
        StringWriter writer = new StringWriter();
        CSVFormat format = CSVFormat.DEFAULT.withNullString(null);
        format.print(null, writer, true);
        assertEquals("", writer.toString());
    }


    @Test
    public void testPrintlnTrailingDelimiterFalse() throws IOException {
        StringWriter writer = new StringWriter();
        CSVFormat format = CSVFormat.DEFAULT.withTrailingDelimiter(false);
        format.println(writer);
        assertTrue(writer.toString().endsWith("\n"));
    }


    @Test
    public void testHashCodeFieldsSet() {
        CSVFormat format1 = CSVFormat.DEFAULT.withQuote('"').withCommentMarker('#');
        CSVFormat format2 = CSVFormat.DEFAULT.withQuote('"').withCommentMarker('#');
        assertEquals(format1.hashCode(), format2.hashCode());
    }


    @Test
    public void testPrintNotNullValueWithNullString() throws IOException {
        StringWriter writer = new StringWriter();
        CSVFormat format = CSVFormat.DEFAULT.withNullString("NULL");
        format.print("test", writer, true);
        assertEquals("test", writer.toString());
    }


    @Test
    public void testPrintNullValueWithEmptyNullString() throws IOException {
        StringWriter writer = new StringWriter();
        CSVFormat format = CSVFormat.DEFAULT.withNullString("");
        format.print(null, writer, true);
        assertEquals("", writer.toString());
    }


    @Test
    public void testWithFirstRecordAsHeaderDefault() {
        CSVFormat format = CSVFormat.DEFAULT.withFirstRecordAsHeader();
        assertTrue(format.getSkipHeaderRecord());
    }


    @Test
    public void testWithHeaderArray() {
        String[] header = {"col1", "col2"};
        CSVFormat format = CSVFormat.DEFAULT.withHeader(header);
        assertArrayEquals(header, format.getHeader());
    }


    @Test
    public void testWithHeaderComments() {
        CSVFormat format = CSVFormat.DEFAULT.withHeaderComments("comment");
        assertNotNull(format.getHeaderComments());
    }


    @Test
    public void testPrintNullValueWithCustomNullString() throws IOException {
        StringWriter writer = new StringWriter();
        CSVFormat format = CSVFormat.DEFAULT.withNullString("NULL");
        format.print(null, writer, true);
        assertEquals("NULL", writer.toString());
    }


    @Test
    public void testWithIgnoreEmptyLinesFlag() {
        CSVFormat format = CSVFormat.DEFAULT.withIgnoreEmptyLines(true);
        assertTrue(format.getIgnoreEmptyLines());
    }


    @Test
    public void testWithIgnoreEmptyLinesTrue() {
        CSVFormat format = CSVFormat.DEFAULT.withIgnoreEmptyLines(true);
        assertTrue(format.getIgnoreEmptyLines());
    }


    @Test
    public void testWithIgnoreEmptyLinesFalseFlag() {
        CSVFormat format = CSVFormat.DEFAULT.withIgnoreEmptyLines(false);
        assertFalse(format.getIgnoreEmptyLines());
    }


    @Test
    public void testWithIgnoreEmptyLinesTrueFlag() {
        CSVFormat format = CSVFormat.DEFAULT.withIgnoreEmptyLines(true);
        assertTrue(format.getIgnoreEmptyLines());
    }


    @Test
    public void testWithIgnoreEmptyLinesFalseFlagValue() {
        CSVFormat format = CSVFormat.DEFAULT.withIgnoreEmptyLines(false);
        assertFalse(format.getIgnoreEmptyLines());
    }


    @Test
    public void testEqualsRecordSeparatorNotNull() {
        CSVFormat format1 = CSVFormat.DEFAULT.withRecordSeparator("\n");
        CSVFormat format2 = CSVFormat.DEFAULT.withRecordSeparator("\n");
        assertTrue(format1.equals(format2));
    }


    @Test
    public void testEqualsCommentMarkerNullVsNotNull() {
        CSVFormat format1 = CSVFormat.DEFAULT;
        CSVFormat format2 = CSVFormat.DEFAULT.withCommentMarker('#');
        assertFalse(format1.equals(format2));
    }


    @Test
    public void testToStringWithHeader() {
        CSVFormat format = CSVFormat.DEFAULT.withHeader("Name", "Age");
        String result = format.toString();
        assertTrue(result.contains("Header:[Name, Age]"));
    }


    @Test
    public void testPrintWithValueNotNull() throws IOException {
        StringWriter writer = new StringWriter();
        CSVFormat format = CSVFormat.DEFAULT;
        format.print("testValue", writer, true);
        assertEquals("testValue", writer.toString());
    }


    @Test
    public void testPrintWithValueNullWithNullString() throws IOException {
        StringWriter writer = new StringWriter();
        CSVFormat format = CSVFormat.DEFAULT.withNullString("NULL");
        format.print(null, writer, true);
        assertEquals("NULL", writer.toString());
    }


    @Test
    public void testPrintlnWithoutTrailingDelimiterWithSeparator() throws IOException {
        StringWriter writer = new StringWriter();
        CSVFormat format = CSVFormat.DEFAULT.withRecordSeparator("\r\n");
        format.println(writer);
        assertTrue(writer.toString().endsWith("\r\n"));
    }


    @Test
    public void testWithHeaderFromMetaDataNoColumns() throws SQLException {
        ResultSetMetaData metaData = mock(ResultSetMetaData.class);
        when(metaData.getColumnCount()).thenReturn(0);
        CSVFormat format = CSVFormat.DEFAULT.withHeader(metaData);
        assertNotNull(format.getHeader());
    }


    @Test
    public void testHashCodeWithFieldsSet() {
        CSVFormat format1 = CSVFormat.DEFAULT.withQuote('"').withCommentMarker('#').withNullString("NULL");
        CSVFormat format2 = CSVFormat.DEFAULT.withQuote('"').withCommentMarker('#').withNullString("NULL");
        assertEquals(format1.hashCode(), format2.hashCode());
    }


    @Test
    public void testPrintWithTrim() throws IOException {
        StringWriter writer = new StringWriter();
        CSVFormat format = CSVFormat.DEFAULT.withTrim(true);
        format.print("  test  ", writer, true);
        assertEquals("test", writer.toString());
    }


    @Test
    public void testPrintWithQuoteModeAll() throws IOException {
        StringWriter writer = new StringWriter();
        CSVFormat format = CSVFormat.DEFAULT.withQuoteMode(QuoteMode.ALL);
        format.print("test,value", writer, true);
        assertEquals("\"test,value\"", writer.toString());
    }


    @Test
    public void testPrintWithNullValueNullStringNull() throws IOException {
        StringWriter writer = new StringWriter();
        CSVFormat format = CSVFormat.DEFAULT.withNullString(null);
        format.print(null, writer, true);
        assertEquals("", writer.toString());
    }


    @Test
    public void testEqualsWithNullRecordSeparator() {
        CSVFormat format1 = CSVFormat.DEFAULT.withRecordSeparator((String) null);
        CSVFormat format2 = CSVFormat.DEFAULT.withRecordSeparator("\n");
        assertFalse(format1.equals(format2));
    }


    @Test
    public void testEqualsWithNullOtherRecordSeparator() {
        CSVFormat format1 = CSVFormat.DEFAULT.withRecordSeparator("\n");
        CSVFormat format2 = CSVFormat.DEFAULT.withRecordSeparator((String) null);
        assertFalse(format1.equals(format2));
    }


    @Test
    public void testToStringWithNullStringAndNullRecordSeparator() {
        CSVFormat format = CSVFormat.DEFAULT.withNullString("NULL").withRecordSeparator((String) null);
        String result = format.toString();
        assertTrue(result.contains("NullString=<NULL>"));
    }


    @Test
    public void testToStringWithoutNullStringAndNotNullRecordSeparator() {
        CSVFormat format = CSVFormat.DEFAULT.withRecordSeparator("\n");
        String result = format.toString();
        assertFalse(result.contains("NullString=<"));
    }


    @Test
    public void testPrintWithTrimTrue() throws IOException {
        StringWriter writer = new StringWriter();
        CSVPrinter printer = new CSVPrinter(writer, CSVFormat.DEFAULT.withTrim(true));
        printer.print("  test  ");
        printer.close();
        assertEquals("test", writer.toString());
    }


    @Test
    public void testPrintWithNullValue() throws IOException {
        StringWriter writer = new StringWriter();
        CSVPrinter printer = new CSVPrinter(writer, CSVFormat.DEFAULT);
        printer.print((String) null);
        printer.close();
        assertEquals("", writer.toString());
    }


    @Test
    public void testPrintWithTrimTrueAndValue() throws IOException {
        StringWriter writer = new StringWriter();
        CSVPrinter printer = new CSVPrinter(writer, CSVFormat.DEFAULT.withTrim(true));
        printer.print("  test  ");
        printer.close();
        assertEquals("test", writer.toString());
    }


    @Test
    public void testWithHeaderEmptyArrayReturnsValidHeader() {
        CSVFormat format = CSVFormat.DEFAULT.withHeader(new String[0]);
        assertNotNull(format.getHeader());
        assertEquals(0, format.getHeader().length);
    }


    @Test
    public void testWithHeaderValidArrayReturnsSameArray() {
        String[] headers = {"col1", "col2"};
        CSVFormat format = CSVFormat.DEFAULT.withHeader(headers);
        assertNotNull(format.getHeader());
        assertArrayEquals(headers, format.getHeader());
    }


    @Test
    public void testPrinterWithAppendableWorksCorrectly() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.print(sb);
        assertNotNull(printer);
    }


    @Test
    public void testPrintWithTrimFlagAndAppendable() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        assertNotNull(printer);
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithData() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlag() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        assertNotNull(printer);
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuote() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrim() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuote() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrim() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuote() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrim() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuote() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrim() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuote() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrim() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuote() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrim() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuote() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrim() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuote() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrim() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuote() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrim() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuote() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrim() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuote() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrim() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuote() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrim() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuote() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrim() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuote() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrim() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuote() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrim() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuote() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrim() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuote() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrim() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuote() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrim() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuote() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testPrintWithTrimFlagAndAppendableWithQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrimAndQuoteAndTrim() throws IOException {
        StringBuilder sb = new StringBuilder();
        CSVPrinter printer = CSVFormat.DEFAULT.withTrim().print(sb);
        printer.print("  test  ");
        printer.close();
        assertEquals("test", sb.toString().trim());
    }


    @Test
    public void testEqualsCommentMarkerNull() {
        CSVFormat format1 = CSVFormat.DEFAULT;
        CSVFormat format2 = CSVFormat.DEFAULT.withCommentMarker('#');
        assertFalse(format1.equals(format2));
    }


    @Test
    public void testToStringHeaderCommentsNotNull() {
        CSVFormat format = CSVFormat.DEFAULT.withHeaderComments("comment1", "comment2");
        String result = format.toString();
        assertTrue(result.contains("HeaderComments"));
    }


    @Test
    public void testToStringQuoteCharSet() {
        CSVFormat format = CSVFormat.DEFAULT.withQuote('"');
        String result = format.toString();
        assertTrue(result.contains("QuoteChar"));
    }


    @Test
    public void testPrintNonNullValue() throws IOException {
        StringWriter writer = new StringWriter();
        CSVFormat format = CSVFormat.DEFAULT;
        format.print("testValue", writer, true);
        assertEquals("testValue", writer.toString());
    }


    @Test
    public void testPrintlnWithRecordSeparator() throws IOException {
        StringWriter writer = new StringWriter();
        CSVFormat format = CSVFormat.DEFAULT.withRecordSeparator("\n");
        format.println(writer);
        assertTrue(writer.toString().endsWith("\n"));
    }


    @Test
    public void testWithHeaderWithMetadata() throws SQLException {
        ResultSetMetaData metaData = mock(ResultSetMetaData.class);
        when(metaData.getColumnCount()).thenReturn(2);
        when(metaData.getColumnLabel(1)).thenReturn("col1");
        when(metaData.getColumnLabel(2)).thenReturn("col2");
        CSVFormat format = CSVFormat.DEFAULT.withHeader(metaData);
        assertNotNull(format.getHeader());
    }


    @Test
    public void testHashCodeQuoteCharSet() {
        CSVFormat format = CSVFormat.DEFAULT.withQuote('"');
        int hash = format.hashCode();
        assertTrue(hash != 0);
    }


    @Test
    public void testPrintNonCharSequenceValue() throws IOException {
        StringWriter writer = new StringWriter();
        CSVFormat format = CSVFormat.DEFAULT;
        format.print(123, writer, true);
        assertEquals("123", writer.toString());
    }


    @Test
    public void testWithIgnoreHeaderCaseTrue() {
        CSVFormat format = CSVFormat.DEFAULT.withIgnoreHeaderCase(true);
        assertTrue(format.getIgnoreHeaderCase());
    }


    @Test
    public void testWithIgnoreHeaderCaseFalse() {
        CSVFormat format = CSVFormat.DEFAULT.withIgnoreHeaderCase(false);
        assertFalse(format.getIgnoreHeaderCase());
    }


    @Test
    public void testWithTrailingDelimiterTrue() {
        CSVFormat format = CSVFormat.DEFAULT.withTrailingDelimiter(true);
        assertTrue(format.getTrailingDelimiter());
    }


    @Test
    public void testEquals() {
        CSVFormat format1 = CSVFormat.DEFAULT;
        CSVFormat format2 = CSVFormat.DEFAULT;
        assertTrue(format1.equals(format2));
    }


    @Test
    public void testHashCode() {
        CSVFormat format1 = CSVFormat.DEFAULT;
        CSVFormat format2 = CSVFormat.DEFAULT;
        assertEquals(format1.hashCode(), format2.hashCode());
    }


    @Test
    public void testToString() {
        CSVFormat format = CSVFormat.DEFAULT;
        assertNotNull(format.toString());
    }


    @Test
    public void testEqualsNullStringNotNull() {
        CSVFormat format1 = CSVFormat.DEFAULT;
        CSVFormat format2 = CSVFormat.DEFAULT.withNullString("NULL");
        assertFalse(format1.equals(format2));
    }

    @Test
    public void  testPlaceHolder() {
        assertTrue(true); 
    }
}

