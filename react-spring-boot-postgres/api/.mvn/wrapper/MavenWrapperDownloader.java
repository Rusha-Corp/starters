/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

import java.net.Authenticator;
import java.net.PasswordAuthentication;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;

/**
 * Maven wrapper downloader that downloads the Maven wrapper jar if it doesn't exist.
 */
public class MavenWrapperDownloader {

    private static final String DEFAULT_WRAPPER_URL =
            "https://repo.maven.apache.org/maven2/org/apache/maven/wrapper/maven-wrapper/3.2.0/maven-wrapper-3.2.0.jar";

    public static void main(String[] args) {
        if (args.length < 2) {
            System.err.println("Usage: MavenWrapperDownloader <wrapperUrl> <jarPath>");
            System.exit(1);
        }

        String wrapperUrl = args[0];
        String jarPath = args[1];

        System.out.println("Downloading Maven wrapper from: " + wrapperUrl);
        System.out.println("Downloading to: " + jarPath);

        try {
            URI uri = URI.create(wrapperUrl);
            HttpClient client = HttpClient.newBuilder()
                    .followRedirects(HttpClient.Redirect.NORMAL)
                    .authenticator(new Authenticator() {
                        @Override
                        protected PasswordAuthentication getPasswordAuthentication() {
                            return super.getPasswordAuthentication();
                        }
                    })
                    .build();

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(uri)
                    .GET()
                    .build();

            HttpResponse<Path> response = client.send(
                    request,
                    HttpResponse.BodyHandlers.ofFile(Paths.get(jarPath), StandardCopyOption.REPLACE_EXISTING)
            );

            if (response.statusCode() != 200) {
                System.err.println("Failed to download Maven wrapper: HTTP " + response.statusCode());
                Files.deleteIfExists(Paths.get(jarPath));
                System.exit(1);
            }

            System.out.println("Download complete.");
        } catch (Exception e) {
            System.err.println("Error downloading Maven wrapper: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
}
