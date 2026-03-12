package com.google.gson.internal.bind;


import org.junit.Before;
import org.junit.After;
import org.junit.Test;
import static org.junit.Assert.*;
import com.google.gson.JsonParser;
import com.google.gson.JsonElement;
import static org.junit.Assert.assertNotNull;

public class JsonTreeReaderTest {


    @Test
    public void testBasicParsing() {
        String json = "{\"name\":\"John\",\"age\":30}";
        com.google.gson.JsonElement element = com.google.gson.JsonParser.parseString(json);
        assertNotNull(element);
    }

    @Test
    public void  testPlaceHolder() {
        assertTrue(true); 
    }
}

