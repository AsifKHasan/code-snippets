function qa_error(description, link=null, where=null, location=null){
  return [where, location, 'error', description, link];
};

function qa_warn(description, link=null, where=null, location=null){
  return [where, location, 'warn', description, link];
};

function qa_todo(description, link=null, where=null, location=null){
  return [where, location, 'todo', description, link];
};

function qa_none(description, link=null, where=null, location=null){
  return [where, location, null, description, link];
};
