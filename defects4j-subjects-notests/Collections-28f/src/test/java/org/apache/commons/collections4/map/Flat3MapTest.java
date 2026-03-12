package org.apache.commons.collections4.map;


import org.junit.Before;
import org.junit.After;
import org.junit.Test;
import static org.junit.Assert.*;
import java.util.Map;
import java.util.Iterator;
import java.util.Map;
import java.util.AbstractMap;

public class Flat3MapTest {


    @Test
    public void testIteratorWithOneEntry() {
        Flat3Map<String, String> map = new Flat3Map<>();
        map.put("key1", "value1");
        
        java.util.Iterator<java.util.Map.Entry<String, String>> iterator = map.entrySet().iterator();
        assertTrue(iterator.hasNext());
        java.util.Map.Entry<String, String> entry = iterator.next();
        assertEquals("key1", entry.getKey());
        assertEquals("value1", entry.getValue());
        assertFalse(iterator.hasNext());
    }


    @Test
    public void testIteratorWithThreeEntries() {
        Flat3Map<String, String> map = new Flat3Map<>();
        map.put("key1", "value1");
        map.put("key2", "value2");
        map.put("key3", "value3");
        
        java.util.Iterator<java.util.Map.Entry<String, String>> iterator = map.entrySet().iterator();
        int count = 0;
        while (iterator.hasNext()) {
            java.util.Map.Entry<String, String> entry = iterator.next();
            assertNotNull(entry.getKey());
            assertNotNull(entry.getValue());
            count++;
        }
        assertEquals(3, count);
    }


    @Test
    public void testRemoveWithOneEntry() {
        Flat3Map<String, String> map = new Flat3Map<>();
        map.put("key1", "value1");
        
        String removedValue = map.remove("key1");
        assertEquals("value1", removedValue);
        assertEquals(0, map.size());
        assertFalse(map.containsKey("key1"));
    }


    @Test
    public void testRemoveWithThreeEntries() {
        Flat3Map<String, String> map = new Flat3Map<>();
        map.put("key1", "value1");
        map.put("key2", "value2");
        map.put("key3", "value3");
        
        String removedValue = map.remove("key2");
        assertEquals("value2", removedValue);
        assertEquals(2, map.size());
        assertFalse(map.containsKey("key2"));
        assertTrue(map.containsKey("key1"));
        assertTrue(map.containsKey("key3"));
    }


    @Test
    public void testClear() {
        Flat3Map<String, String> map = new Flat3Map<>();
        map.put("key1", "value1");
        map.put("key2", "value2");
        map.put("key3", "value3");
        
        map.clear();
        assertEquals(0, map.size());
        assertTrue(map.isEmpty());
    }


    @Test
    public void testContainsKeyWithExistingKeys() {
        Flat3Map<String, String> map = new Flat3Map<>();
        map.put("key1", "value1");
        map.put("key2", "value2");
        map.put("key3", "value3");
        
        assertTrue(map.containsKey("key1"));
        assertTrue(map.containsKey("key2"));
        assertTrue(map.containsKey("key3"));
    }


    @Test
    public void testContainsKeyWithNonExistingKeys() {
        Flat3Map<String, String> map = new Flat3Map<>();
        map.put("key1", "value1");
        map.put("key2", "value2");
        map.put("key3", "value3");
        
        assertFalse(map.containsKey("key4"));
        assertFalse(map.containsKey("key5"));
    }


    @Test
    public void testContainsValueWithExistingValues() {
        Flat3Map<String, String> map = new Flat3Map<>();
        map.put("key1", "value1");
        map.put("key2", "value2");
        map.put("key3", "value3");
        
        assertTrue(map.containsValue("value1"));
        assertTrue(map.containsValue("value2"));
        assertTrue(map.containsValue("value3"));
    }


    @Test
    public void testContainsValueWithNonExistingValues() {
        Flat3Map<String, String> map = new Flat3Map<>();
        map.put("key1", "value1");
        map.put("key2", "value2");
        map.put("key3", "value3");
        
        assertFalse(map.containsValue("value4"));
        assertFalse(map.containsValue("value5"));
    }


    @Test
    public void testSizeWithOneEntry() {
        Flat3Map<String, String> map = new Flat3Map<>();
        map.put("key1", "value1");
        
        assertEquals(1, map.size());
    }


    @Test
    public void testSizeWithThreeEntries() {
        Flat3Map<String, String> map = new Flat3Map<>();
        map.put("key1", "value1");
        map.put("key2", "value2");
        map.put("key3", "value3");
        
        assertEquals(3, map.size());
    }


    @Test
    public void testIsEmptyWhenNotEmpty() {
        Flat3Map<String, String> map = new Flat3Map<>();
        map.put("key1", "value1");
        
        assertFalse(map.isEmpty());
    }


    @Test
    public void testGetWhenKeyExists() {
        Flat3Map<String, String> map = new Flat3Map<>();
        map.put("key1", "value1");
        
        assertEquals("value1", map.get("key1"));
    }


    @Test
    public void testGetWhenKeyDoesNotExist() {
        Flat3Map<String, String> map = new Flat3Map<>();
        map.put("key1", "value1");
        
        assertNull(map.get("key2"));
    }


    @Test
    public void testPutWhenReplacingExistingKey() {
        Flat3Map<String, String> map = new Flat3Map<>();
        map.put("key1", "value1");
        String oldValue = map.put("key1", "value2");
        
        assertEquals("value1", oldValue);
        assertEquals("value2", map.get("key1"));
    }


    @Test
    public void testPutWhenAddingNewKey() {
        Flat3Map<String, String> map = new Flat3Map<>();
        map.put("key1", "value1");
        String oldValue = map.put("key2", "value2");
        
        assertNull(oldValue);
        assertEquals("value2", map.get("key2"));
    }


    @Test
    public void testEntrySetWithOneEntry() {
        Flat3Map<String, String> map = new Flat3Map<>();
        map.put("key1", "value1");
        
        assertEquals(1, map.entrySet().size());
        assertTrue(map.entrySet().contains(new java.util.AbstractMap.SimpleEntry<>("key1", "value1")));
    }


    @Test
    public void testEntrySetWithThreeEntries() {
        Flat3Map<String, String> map = new Flat3Map<>();
        map.put("key1", "value1");
        map.put("key2", "value2");
        map.put("key3", "value3");
        
        assertEquals(3, map.entrySet().size());
        assertTrue(map.entrySet().contains(new java.util.AbstractMap.SimpleEntry<>("key1", "value1")));
        assertTrue(map.entrySet().contains(new java.util.AbstractMap.SimpleEntry<>("key2", "value2")));
        assertTrue(map.entrySet().contains(new java.util.AbstractMap.SimpleEntry<>("key3", "value3")));
    }

    @Test
    public void  testPlaceHolder() {
        assertTrue(true); 
    }
}

