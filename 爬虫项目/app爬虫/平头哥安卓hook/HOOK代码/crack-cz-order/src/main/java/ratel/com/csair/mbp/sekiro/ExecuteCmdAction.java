package ratel.com.csair.mbp.sekiro;

import com.virjar.ratel.api.extension.FileLogger;
import com.virjar.ratel.api.inspect.Lists;
import com.virjar.sekiro.api.ActionHandler;
import com.virjar.sekiro.api.SekiroRequest;
import com.virjar.sekiro.api.SekiroResponse;
import com.virjar.sekiro.api.databind.AutoBind;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Collections;
import java.util.List;

import external.org.apache.commons.lang3.StringUtils;

public class ExecuteCmdAction implements ActionHandler {
    @Override
    public String action() {
        return "exec";
    }

    @AutoBind
    private String cmd;

    @Override
    public void handleRequest(SekiroRequest sekiroRequest, final SekiroResponse sekiroResponse) {

        new Thread() {
            @Override
            public void run() {
                try {
                    Process process = Runtime.getRuntime().exec(cmd);

                    List<String> res = Collections.synchronizedList(Lists.<String>newLinkedList());

                    StreamGobbler STDOUT = new StreamGobbler("std-", process.getInputStream(),
                            res);
                    StreamGobbler STDERR = new StreamGobbler("error*", process.getErrorStream(),
                            res);

                    // start gobbling and write our commands to the shell
                    STDOUT.start();
                    STDERR.start();

                    process.waitFor();

                    STDOUT.join();
                    STDERR.join();
                    process.destroy();

                    sekiroResponse.send(StringUtils.join(res, "\n"));

                } catch (Exception e) {
                    sekiroResponse.failed(FileLogger.getTrack(e));
                }
            }
        }.start();

    }


    /**
     * Line callback interface
     */
    public interface OnLineListener {
        /**
         * <p>Line callback</p>
         * <p>
         * <p>This callback should process the line as quickly as possible.
         * Delays in this callback may pause the native process or even
         * result in a deadlock</p>
         *
         * @param line String that was gobbled
         */
        void onLine(String line);
    }

    /**
     * Thread utility class continuously reading from an InputStream
     */

    public static class StreamGobbler extends Thread {


        private String shell = null;
        private BufferedReader reader = null;
        private List<String> writer = null;
        private ExecuteCmdAction.OnLineListener listener = null;

        /**
         * <p>StreamGobbler constructor</p>
         * <p>
         * <p>We use this class because shell STDOUT and STDERR should be read as quickly as
         * possible to prevent a deadlock from occurring, or Process.waitFor() never
         * returning (as the buffer is full, pausing the native process)</p>
         *
         * @param shell       Name of the shell
         * @param inputStream InputStream to read from
         * @param outputList  {@literal List<String>} to write to, or null
         */
        public StreamGobbler(String shell, InputStream inputStream, List<String> outputList) {
            this.shell = shell;
            reader = new BufferedReader(new InputStreamReader(inputStream));
            writer = outputList;
        }

        /**
         * <p>StreamGobbler constructor</p>
         * <p>
         * <p>We use this class because shell STDOUT and STDERR should be read as quickly as
         * possible to prevent a deadlock from occurring, or Process.waitFor() never
         * returning (as the buffer is full, pausing the native process)</p>
         *
         * @param shell          Name of the shell
         * @param inputStream    InputStream to read from
         * @param onLineListener OnLineListener callback
         */
        public StreamGobbler(String shell, InputStream inputStream, ExecuteCmdAction.OnLineListener onLineListener) {
            this.shell = shell;
            reader = new BufferedReader(new InputStreamReader(inputStream));
            listener = onLineListener;
        }

        @Override
        public void run() {
            // keep reading the InputStream until it ends (or an error occurs)
            try {
                String line;
                while ((line = reader.readLine()) != null) {
                    if (writer != null) writer.add(line);
                    if (listener != null) listener.onLine(line);
                }
            } catch (IOException e) {
                // reader probably closed, expected exit condition
            }

            // make sure our stream is closed and resources will be freed
            try {
                reader.close();
            } catch (IOException e) {
                // read already closed
            }
        }
    }

}
