import os
from pathlib import Path

error_log_has_new_errors = False

def sanitize_title(title):
  """Sanitize the title to be used as a directory name."""
  return title.replace(" ", "_").replace(":", "").replace("/", "_")

def prettify_title(title):
  """From underscored title, return a title with spaces instead of underscores, with each word capitalized."""
  return title.replace("_", " ").title()

def has_next(sequence, index):
  """Check if there's a next element in a sequence."""
  return index + 1 < len(sequence)

def get_root_directory():
  """Get the root directory of the project."""
  current_dir = Path(__file__).parent.resolve() # src
  parent_dir = os.path.dirname(current_dir) # root of the project
  return parent_dir

def write_to_error_log(contents):
  """Write contents to an error log file."""
  global error_log_has_new_errors
  error_log_path = os.path.join(get_root_directory(), 'error.log')
  error_log_has_new_errors = True
  if not os.path.exists(error_log_path):
    with open(error_log_path, 'w') as f:
      f.write('')
  with open(error_log_path, 'a') as f:
    if not contents.endswith('\n'):
      contents += '\n'
    f.write(contents)
  
def error_log_has_new_errors():
  """Returns true if the error log has new errors during this run."""
  global error_log_has_new_errors;
  return error_log_has_new_errors