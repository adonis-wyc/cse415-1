from TTS_State import TTS_State

USE_CUSTOM_STATIC_EVAL_FUNCTION = False

class MY_TTS_State(TTS_State):
  def static_eval(self):
    if USE_CUSTOM_STATIC_EVAL_FUNCTION:
      return self.custom_static_eval()
    else:
      return self.basic_static_eval()

  def basic_static_eval(self, color, n):
      
    raise Exception("basic_static_eval not yet implemented.")

  def custom_static_eval(self):
    raise Exception("custom_static_eval not yet implemented.")

def get_ready(initial_state, k, what_side_i_play, opponent_moniker):
    return 1

def who_am_i():
    return 'I am me'

def moniker():
    return 'I am the best'

def take_turn(current_state, opponents_utterance, time_limit=10):
    return 'Ok'

def parameterized_minimax(**keywordargs):
    return 'Cool'
    