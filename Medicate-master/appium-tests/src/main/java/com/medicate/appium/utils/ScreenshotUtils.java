package com.medicate.appium.utils;

import io.appium.java_client.AppiumDriver;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import java.io.File;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;
import java.text.SimpleDateFormat;
import java.util.Date;

public class ScreenshotUtils {
    public static String captureScreenshot(AppiumDriver driver, String screenshotName) {
        String dateName = new SimpleDateFormat("yyyyMMddhhmmss").format(new Date());
        TakesScreenshot ts = (TakesScreenshot) driver;
        File source = ts.getScreenshotAs(OutputType.FILE);
        
        File dir = new File(System.getProperty("user.dir") + "/screenshots");
        if (!dir.exists()) {
            dir.mkdirs();
        }
        
        File finalDestination = new File(dir, screenshotName + "_" + dateName + ".png");
        try {
            Files.copy(source.toPath(), finalDestination.toPath(), StandardCopyOption.REPLACE_EXISTING);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return finalDestination.getAbsolutePath();
    }
}
