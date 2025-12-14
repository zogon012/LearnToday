import signal
import sys
import time
import logging
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

class GracefulKiller:
    def __init__(self):
        self.kill_now = False
        self.shutdown_reason: Optional[str] = None
        
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)
        
        logger.info("Signal handlers registered for SIGTERM and SIGINT")
    
    def _handle_signal(self, signum: int, frame) -> None:
        signal_names = {
            signal.SIGTERM: "SIGTERM",
            signal.SIGINT: "SIGINT"
        }
        
        signal_name = signal_names.get(signum, f"Signal {signum}")
        self.shutdown_reason = signal_name
        
        logger.warning(f"Received {signal_name} - Initiating graceful shutdown...")
        self.kill_now = True
    
    def graceful_shutdown(self):
        logger.info("Starting graceful shutdown process...")
        
        logger.info("Saving application state...")
        time.sleep(1)
        
        logger.info("Closing connections...")
        time.sleep(0.5)
        
        logger.info("Cleaning up resources...")
        time.sleep(0.5)
        
        logger.info(f"Graceful shutdown completed (triggered by {self.shutdown_reason})")

def main():
    killer = GracefulKiller()
    
    logger.info("Application starting...")
    logger.info("Send SIGTERM (docker stop) or SIGINT (Ctrl+C) to test graceful shutdown")
    
    counter = 0
    
    while not killer.kill_now:
        counter += 1
        logger.info(f"Working... (iteration {counter})")
        
        for _ in range(10):
            if killer.kill_now:
                break
            time.sleep(0.1)
    
    killer.graceful_shutdown()
    logger.info("Application terminated")

if __name__ == "__main__":
    main()