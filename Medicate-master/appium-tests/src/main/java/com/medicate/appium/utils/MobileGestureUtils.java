package com.medicate.appium.utils;

import io.appium.java_client.AppiumDriver;
import org.openqa.selenium.Dimension;
import org.openqa.selenium.Point;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.PointerInput;
import org.openqa.selenium.interactions.Sequence;
import java.time.Duration;
import java.util.Collections;

public class MobileGestureUtils {
    
    public static void tap(AppiumDriver driver, Point point) {
        PointerInput finger = new PointerInput(PointerInput.Kind.TOUCH, "finger");
        Sequence tapSequence = new Sequence(finger, 1);
        tapSequence.addAction(finger.createPointerMove(Duration.ZERO, PointerInput.Origin.viewport(), point.x, point.y));
        tapSequence.addAction(finger.createPointerDown(PointerInput.MouseButton.LEFT.asArg()));
        tapSequence.addAction(finger.createPointerUp(PointerInput.MouseButton.LEFT.asArg()));
        driver.perform(Collections.singletonList(tapSequence));
    }

    public static void tapElement(AppiumDriver driver, WebElement element) {
        Point location = element.getLocation();
        Dimension size = element.getSize();
        Point center = new Point(location.x + size.width / 2, location.y + size.height / 2);
        tap(driver, center);
    }

    public static void swipe(AppiumDriver driver, Point start, Point end, Duration duration) {
        PointerInput finger = new PointerInput(PointerInput.Kind.TOUCH, "finger");
        Sequence swipeSequence = new Sequence(finger, 1);
        swipeSequence.addAction(finger.createPointerMove(Duration.ZERO, PointerInput.Origin.viewport(), start.x, start.y));
        swipeSequence.addAction(finger.createPointerDown(PointerInput.MouseButton.LEFT.asArg()));
        swipeSequence.addAction(finger.createPointerMove(duration, PointerInput.Origin.viewport(), end.x, end.y));
        swipeSequence.addAction(finger.createPointerUp(PointerInput.MouseButton.LEFT.asArg()));
        driver.perform(Collections.singletonList(swipeSequence));
    }

    public static void swipeUp(AppiumDriver driver) {
        Dimension size = driver.manage().window().getSize();
        Point start = new Point(size.width / 2, (int) (size.height * 0.8));
        Point end = new Point(size.width / 2, (int) (size.height * 0.2));
        swipe(driver, start, end, Duration.ofMillis(600));
    }

    public static void swipeDown(AppiumDriver driver) {
        Dimension size = driver.manage().window().getSize();
        Point start = new Point(size.width / 2, (int) (size.height * 0.2));
        Point end = new Point(size.width / 2, (int) (size.height * 0.8));
        swipe(driver, start, end, Duration.ofMillis(600));
    }

    public static void swipeLeft(AppiumDriver driver) {
        Dimension size = driver.manage().window().getSize();
        Point start = new Point((int) (size.width * 0.8), size.height / 2);
        Point end = new Point((int) (size.width * 0.2), size.height / 2);
        swipe(driver, start, end, Duration.ofMillis(600));
    }

    public static void swipeRight(AppiumDriver driver) {
        Dimension size = driver.manage().window().getSize();
        Point start = new Point((int) (size.width * 0.2), size.height / 2);
        Point end = new Point((int) (size.width * 0.8), size.height / 2);
        swipe(driver, start, end, Duration.ofMillis(600));
    }
}
