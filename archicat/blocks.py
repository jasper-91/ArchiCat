from .block import *
from enum import Enum


def _operation(opcode):
    return Block(opcode,NUM1=float_input,NUM2=float_input)

def _comparison(opcode):
    return Block(opcode,OPERAND1=float_input,OPERAND2=float_input)

def _bool_operation(opcode):
    return Block(opcode,OPERAND1=bool_input,OPERAND2=bool_input)


class GotoOptions(Enum):
    RANDOM = '_random_'
    MOUSE = '_mouse_'

class SetRotationStyleOptions(Enum):
    ALL_AROUND = 'all around'
    LEFT_RIGHT = 'left-right'
    DONT_ROTATE = 'don\'t rotate'

class SwitchBackdropToOptions(Enum):
    NEXT_BACKDROP = 'next backdrop'
    PREVIOUS_BACKDROP = 'previous backdrop'
    RANDOM_BACKDROP = 'random backdrop'

class EffectOptions(Enum):
    COLOR = 'COLOR'
    FISHEYE = 'FISHEYE'
    WHIRL = 'WHIRL'
    PIXELATE = 'PIXELATE'
    MOSAIC = 'MOSAIC'
    BRIGHTNESS = 'BRIGHTNESS'
    GHOST = 'GHOST'

class GoToFrontBackOptions(Enum):
    FRONT = 'front'
    BACK = 'back'

class GoForwardBackwardLayersOptions(Enum):
    FORWARD = 'forward'
    BACKWARD = 'backward'

class NumberNameOptions(Enum):
    NUMBER = 'number'
    NAME = 'name'

class SoundEffectOptions(Enum):
    PITCH = 'PITCH'
    PAN = 'PAN'

class MathOpOptions(Enum):
    ABS = 'abs'
    FLOOR = 'floor'
    CEILING = 'ceiling'
    SQRT = 'sqrt'
    SIN = 'sin'
    COS = 'cos'
    TAN = 'tan'
    ASIN = 'asin'
    ACOS = 'acos'
    ATAN = 'atan'
    POWER_E = 'e ^'
    POWER_10 = '10 ^'

class CreateCloneOfOptions(Enum):
    MYSELF = '_myself_'

class StopOptions(Enum):
    ALL = 'all'
    THIS_SCRIPT = 'this script'
    OTHER_SCRIPTS = 'other scripts in sprite'

class WhenGreaterThanOptions(Enum):
    LOUDNESS = 'LOUDNESS'
    TIMER = 'TIMER'

class TouchingObjectOptions(Enum):
    MOUSE = '_mouse_'
    EDGE = '_edge_'

class DistanceToOptions(Enum):
    MOUSE = '_mouse_'

class SetDragModeOptions(Enum):
    DRAGGABLE = 'draggable'
    NOT_DRAGGABLE = 'not draggable'

class OfOptions(Enum):
    STAGE = '_stage_'
    X = 'x position'
    Y = 'y position'
    DIRECTION = 'direction'
    COSTUME_NUMBER = 'costume #'
    COSTUME_NAME = 'costume name'
    BACKDROP_NUMBER = 'backdrop #'
    BACKDROP_NAME = 'backdrop name'
    SIZE = 'size'
    VOLUME = 'volume'

class CurrentOptions(Enum):
    YEAR = 'YEAR'
    MONTH = 'MONTH'
    DATE = 'DATE'
    DAY_OF_WEEK = 'DAYOFWEEK'
    HOUR = 'HOUR'
    MINUTE = 'MINUTE'
    SECOND = 'SECOND'


class GoTo(Block):
    sub_block_opcode: str

    def __init__(self):
        super().__init__('motion_goto')
        self.sub_block_opcode = 'motion_goto_menu'

    def _sub_block(self,builder: ScratchFileBuilder,sprite: str) -> components.Id:
        return builder._register_block(components.Block(self.sub_block_opcode,
                                                        fields = {'TO': components.Field(sprite)},shadow=True))
    
    def __call__(self,builder: ScratchFileBuilder,sprite: str | GotoOptions | components.Id,id: Optional[components.Id] = None) -> components.Id:
        if isinstance(sprite,components.Id):
            block = components.Block(self.opcode,inputs = {'TO': input(builder,components.InputType.OBSCURED_SHADOW,
                                                sprite,self._sub_block(builder,GotoOptions.RANDOM.value))})
        elif isinstance(sprite,GotoOptions):
            block = components.Block(self.opcode,inputs = {'TO': input(builder,components.InputType.SHADOW,
                                                self._sub_block(builder,sprite.value))})
        else:
            block = components.Block(self.opcode,inputs = {'TO': input(builder,components.InputType.SHADOW,
                                                self._sub_block(builder,sprite))})
        return builder._register_block(block,id=id)
    

class GlideTo(GoTo):
    def __init__(self):
        super().__init__()
        self.opcode = 'motion_glideto'
        self.sub_block_opcode = 'motion_glideto_menu'


class PointTowards(GoTo):
    def __init__(self):
        super().__init__()
        self.opcode = 'motion_pointtowards'
        self.sub_block_opcode = 'motion_pointtowardsmenu'


class SwitchCostumeTo(Block):
    def __init__(self):
        super().__init__('looks_switchcostumeto')

    def _sub_block(self,builder: ScratchFileBuilder,costume: str) -> components.Id:
        return builder._register_block(components.Block('looks_costume',
                                                        fields = {'COSTUME': components.Field(costume)},shadow=True))

    def __call__(self,builder: ScratchFileBuilder,costume: str | components.Id) -> components.Id:
        if isinstance(costume,components.Id):
            block = components.Block(self.opcode,inputs = {'COSTUME': input(builder,components.InputType.OBSCURED_SHADOW,
                                                self._sub_block(builder,builder.current_target.costumes[0].name))})
        else:
            block = components.Block(self.opcode,inputs = {'COSTUME': input(builder,components.InputType.SHADOW,
                                                                           self._sub_block(builder,costume))})
        return builder._register_block(block,id=id)
    

class SwitchBackdropTo(Block):
    def __init__(self):
        super().__init__('looks_switchbackdropto')

    def _sub_block(self,builder: ScratchFileBuilder,backdrop: str) -> components.Id:
        return builder._register_block(components.Block('looks_backdrops',
                                                        fields = {'BACKDROP': components.Field(backdrop)},shadow=True))

    def __call__(self,builder: ScratchFileBuilder,backdrop: str | components.Id | SwitchBackdropToOptions,id: Optional[components.Id] = None) -> components.Id:
        if isinstance(backdrop,components.Id):
            block = components.Block(self.opcode,inputs = {'BACKDROP': input(builder,components.InputType.OBSCURED_SHADOW,
                                                self._sub_block(backdrop,builder.current_target.costumes[0].name))})
        elif isinstance(backdrop,SwitchBackdropToOptions):
            block = components.Block(self.opcdoe,inputs = {'BACKDROP': input(builder,components.SHADOW,
                                                                            self._sub_block(builder,backdrop.value))})
        else:
            block = components.Block(self.opcode,inputs = {'BACKDROP': input(builder,components.InputType.SHADOW,
                                                                           self._sub_block(builder,backdrop))})
        return builder._register_block(block,id=id)
    

class SwitchBackdropToAndWait(SwitchBackdropTo):
    def __init__(self):
        super().__init__()
        self.opcode = 'looks_switchbackdroptoandwait'


class PlayUntilDone(Block):
    def __init__(self):
        super().__init__('sound_playuntildone')

    def _sub_block(self,builder: ScratchFileBuilder,sound: str) -> components.Id:
        return builder._register_block(components.Block('sound_sounds_menu',fields = {'SOUND_MENU': components.Field(sound)},shadow=True))
    
    def __call__(self,builder: ScratchFileBuilder,sound: str | components.Id,id: Optional[components.Id] = None) -> components.Id:
        if isinstance(sound,components.Id):
            block = components.Block(self.opcode,inputs = {'SOUND_MENU': input(builder,components.InputType.OBSCURED_SHADOW,
                                                        sound,self._sub_block(builder,builder.current_target.sounds[0].name))})
        else:
            block = components.Block(self.opcode,inputs = {'SOUND_MENU': input(builder,components.InputType.SHADOW,
                                                        self._sub_block(builder,sound))})
        return builder._register_block(block,id=id)
    

class Play(PlayUntilDone):
    def __init__(self):
        super().__init__()
        self.opcode = 'sound_play'


class Broadcast(Block):
    def __init__(self):
        super().__init__('event_broadcast')

    def _sub_block(self,builder: ScratchFileBuilder,broadcast: str) -> components.VariableValue:
        return components.VariableValue(components.VariableType.MESSAGE,broadcast,builder._get_message(broadcast))

    def __call__(self,builder: ScratchFileBuilder,message: str | components.Id,id: Optional[components.Id] = None) -> components.Id:
        if isinstance(message,components.Id):
            block = components.Block(self.opcode,inputs = {'BROADCAST_INPUT': input(builder,components.InputType.OBSCURED_SHADOW,
                                                message,self._sub_block(builder,next(builder.stage.broadcasts.keys())))})
        else:
            block = components.Block(self.opcode,inputs = {'BROADCAST_INPUT': input(builder,components.InputType.SHADOW,
                                                self._sub_block(builder,message))})
        return builder._register_block(block,id=id)
    

class BroadcastAndWait(Broadcast):
    def __init__(self):
        super().__init__()
        self.opcode = 'event_broadcastandwait'


class Stop(Block):
    def __init__(self):
        super().__init__('control_stop')

    def __call__(self,builder: ScratchFileBuilder,option: StopOptions | str,id: Optional[components.Id] = None) -> components.Id:
        option = StopOptions(option) if isinstance(option,str) else option
        return builder._register_block(components.MutationBlock('control_stop_menu',
                        fields = {'STOP_OPTIONS': components.Field(option.value)},
                        mutation=components.ControlStop(components.HasNext.FALSE if option == StopOptions.OTHER_SCRIPTS 
                                                        else components.HasNext.TRUE)),id=id)


class CreateCloneOf(Block):
    def __init__(self):
        super().__init__('control_create_clone_of')

    def _sub_block(self,builder: ScratchFileBuilder,option: str) -> components.Id:
        return builder._register_block(components.Block('control_create_clone_of_menu',
                                                        fields = {'CLONE_OPTION': components.Field(option)},shadow=True))

    def __call__(self,builder: ScratchFileBuilder,option: CreateCloneOfOptions | str | components.Id,id: Optional[components.Id] = None) -> components.Id:
        if isinstance(option,components.Id):
             block = components.Block(self.opcode,
                inputs = {'CLONE_OPTION': input(builder,components.InputType.OBSCURED_SHADOW,option,
                                                           self._sub_block(builder,CreateCloneOfOptions.MYSELF))})
        elif isinstance(option,CreateCloneOfOptions):
            block = self.__call__(builder,option.value)
        else:
            block = components.Block(self.opcode,
                    inputs = {'CLONE_OPTION': input(builder,components.InputType.SHADOW,self._sub_block(builder,option))
                })
        return builder._register_block(block,id=id)
    

class TouchingObject(Block):
    def __init__(self):
        super().__init__('sensing_touchingobject')

    def _sub_block(self,builder: ScratchFileBuilder,object: str) -> components.Id:
        return builder._register_block(components.Block('sensing_touchingobjectmenu',
                                        fields = {'TOUCHINGOBJECTMENU': components.Field(object)},shadow=True))
    
    def __call__(self,builder: ScratchFileBuilder,object: TouchingObjectOptions | str | components.Id,id: Optional[components.Id] = None) -> components.Id:
        if isinstance(object,components.Id):
            block = components.Block('sensing_touchingobject',inputs = {'TOUCHINGOBJECTMENU': input(builder,components.InputType.OBSCURED_SHADOW,
                                                            object,self._sub_block(builder,object))})
        elif isinstance(object,TouchingObjectOptions):
            block = components.Block('sensing_touchingobject',inputs = {'TOUCHINGOBJECTMENU': input(builder,components.InputType.SHADOW,
                                                                                                    self._sub_block(builder,object.value))})
        else:
            block = components.Block('sensing_touchingobject',inputs = {'TOUCHINGOBJECTMENU': input(builder,components.InputType.SHADOW,
                                                                                                    self._sub_block(builder,object))})
        return builder._register_block(block,id=id)
    

class KeyPressed(Block):
    def __init__(self):
        super().__init__('sensing_keypressed')

    def _sub_block(self,builder: ScratchFileBuilder,key: str) -> components.Id:
        return builder._register_block(components.Block('sensing_keyoptions',fields = {'KEY_OPTION': components.Field(key)},shadow=True))
    
    def __call__(self,builder: ScratchFileBuilder,key: str | components.Id,id: Optional[components.Id] = None) -> components.Id:
        if isinstance(key,components.Id):
            block = components.Block('sensing_keypressed',inputs = {'KEY_OPTION': input(builder,components.InputType.OBSCURED_SHADOW,
                                                        key,self._sub_block(builder,'space'))})
        else:
            block = components.Block('sensing_keypressed',inputs = {'KEY_OPTION': input(builder,components.InputType.SHADOW,
                                                        self._sub_block(builder,key))})
        return builder._register_block(block,id=id)
    

class DistanceTo(Block):
    def __init__(self):
        super().__init__('sensing_distanceto')

    def _sub_block(self,builder: ScratchFileBuilder,object: str) -> components.Id:
        return builder._register_block(components.Block('sensing_distancetooptions',fields = {'DISTANCETOMENU': components.Field(object)},shadow=True))
    
    def __call__(self,builder: ScratchFileBuilder,object: str | components.Id | DistanceToOptions,id: Optional[components.Id] = None) -> components.Id:
        if isinstance(object,components.Id):
            block = components.Block(self.opcode,inputs = {'DISTANCETOMENU': components.Input(components.InputType.OBSCURED_SHADOW,
                                                                self._sub_block(builder,object),self._sub_block(builder,'_mouse_'))})
        elif isinstance(object,str):
            block = components.Block(self.opcode,inputs = {'DISTANCETOMENU': components.Input(components.InputType.SHADOW,
                                                                self._sub_block(object))})
        else:
            block = components.Block(self.opcode,inputs = {'DISTANCETOMENU': components.Input(components.InputType.SHADOW,
                                                                self._sub_block(object.value))})
        return builder._register_block(block,id=id)

class Of(Block):
    def __init__(self):
        super().__init__('sensing_of')

    def _sub_block(self,builder: ScratchFileBuilder,object: str) -> components.Id:
        return builder._register_block(components.Block('sensing_of_object_menu',fields = {'OBJECT': components.Field(object)},shadow=True))
    
    def __call__(self,builder: ScratchFileBuilder,object: str | components.Id | OfOptions,member: str | OfOptions,id: Optional[components.Id] = None) -> components.Id:
        def member_field(member):
            if isinstance(member,str):
                return components.Field(member)
            else:
                return components.Field(member.value)
            
        if isinstance(object,components.Id):
            block = components.Block('sensing_of',inputs = {'OBJECT': input(builder,components.InputType.OBSCURED_SHADOW,
                                                object,self._sub_block(builder,OfOptions.STAGE.value))},
                                                fields = {'PROPERTY': member_field(member)})
        elif isinstance(object,OfOptions):
            block = components.Block('sensing_of',inputs = {'OBJECT': input(builder,components.InputType.SHADOW,
                                                self._sub_block(builder,object.value))},
                                                fields = {'PROPERTY': member_field(member)})
        else:
            block = components.Block('sensing_of',inputs = {'OBJECT': input(builder,components.InputType.SHADOW,
                                                self._sub_block(builder,object))},
                                                fields = {'PROPERTY': member_field(member)})
        return builder._register_block(block,id=id)
    

class Current(MonitorableBlock):
    def monitor(self,builder: ScratchFileBuilder,*args: InputItem,
                x: int = 0,y: int = 0,visible: bool = True,):
        block = super().monitor(builder,*args,x=x,y=y,visible=visible)
        block.id = 'current_' + block.params['CURRENTMENU'].lower()
        return block
    

class Variable(MonitorableBlock):
    sprite_specific = False

    def monitor(self,builder: ScratchFileBuilder,*args: InputItem,
                x: int = 0,y: int = 0,visible: bool = True,mode: str = 'default',
                sliderMin: int = 0,sliderMax: int = 100,isDiscrete: bool = True) -> components.Monitor:
        monitor = super().monitor(builder,*args,x,y,visible)
        monitor.id = builder._get_variable(monitor.params['VARIABLE'])
        if any(variable.name == monitor.params['VARIABLE'] for variable in builder.current_target.variables.values()):
            monitor.spriteName = builder.current_target.name
        monitor.mode = mode
        monitor.sliderMin = sliderMin
        monitor.sliderMax = sliderMax
        monitor.isDiscrete = isDiscrete
        return monitor


class List(MonitorableBlock):
    sprite_specific = False

    def monitor(self,builder: ScratchFileBuilder,*args: InputItem,
                x: int = 0,y: int = 0,visible: bool = True,width: int = 100,height = 100) -> components.Monitor:
        monitor = components.ListMonitor(**vars(super().monitor(builder,*args,x,y,visible)))
        monitor.id = builder._get_list(monitor.params['LIST'])
        if any(list.name == monitor.params['LIST'] for list in builder.current_target.lists.values()):
            monitor.spriteName = builder.current_target.name
        monitor.value = []
        monitor.opcode = 'data_listcontents'
        monitor.mode = 'list'
        monitor.width = width
        monitor.height = height
        return monitor


statement_blocks = {
    # Looks
    'SwitchBackdropTo': SwitchBackdropTo().attach_option(SwitchBackdropToOptions),
    # Sounds
    'PlayUntilDone': PlayUntilDone(),
    'Play': Play(),
    'StopAllSounds': Block('sound_stopallsounds'),
    'ChangeSoundEffectBy': Block('sound_changeeffectby',EFFECT=option_field(SoundEffectOptions),VALUE=float_input).attach_option(SoundEffectOptions),
    'SetSoundEffectTo': Block('sound_seteffectto',EFFECT=option_field(SoundEffectOptions),VALUE=float_input).attach_option(SoundEffectOptions),
    'ClearSoundEffects': Block('sound_cleareffects'),
    'ChangeVolumeBy': Block('sound_changevolumeby',VOLUME=float_input),
    'SetVolumeTo': Block('sound_setvolumeto',VOLUME=float_input),
    'Volume': MonitorableBlock('sound_volume'),
    # Control
    'Wait': Block('control_wait',DURATION=unsigned_float_input),
    'Repeat': Block('control_repeat',TIMES=unsigned_int_input,SUBSTACK=chain_input),
    'Forever': Block('control_forever',SUBSTACK=chain_input),
    'If': Block('control_if',CONDITION=bool_input,SUBSTACK=chain_input),
    'IfElse': Block('control_if_else',CONDITION=bool_input,SUBSTACK=chain_input,SUBSTACK2=chain_input),
    'WaitUntil': Block('control_wait_until',CONDITION=bool_input),
    'RepeatUntil': Block('control_repeat_until',CONDITION=bool_input,SUBSTACK=chain_input),
    'Stop': Stop().attach_option(StopOptions),
    'CreateCloneOf': CreateCloneOf().attach_option(CreateCloneOfOptions),
    # Event
    'Broadcast': Broadcast(),
    'BroadcastAndWait': BroadcastAndWait(),
    # Sensing
    'SetDragMode': Block('sensing_setdragmode',DRAG_MODE=option_field(SetDragModeOptions)).attach_option(SetDragModeOptions),
    # Data
    'SetVariableTo': Block('data_setvariableto',VARIABLE=variable_field,VALUE=string_input),
    'ChangeVariableBy': Block('data_changevariableby',VARIABLE=variable_field,VALUE=float_input),
    'ShowVariable': Block('data_showvariable',VARIABLE=variable_field),
    'HideVariable': Block('data_hidevariable',VARIABLE=variable_field),
    'AddToList': Block('data_addtolist',LIST=list_field,ITEM=string_input),
    'DeleteOfList': Block('data_deleteoflist',LIST=list_field,INDEX=unsigned_int_input),
    'DeleteAllOfList': Block('data_deletealloflist',LIST=list_field),
    'InsertAtList': Block('data_insertatlist',LIST=list_field,INDEX=unsigned_int_input,VALUE=string_input),
    'ReplaceItemOfList': Block('data_replaceitemoflist',LIST=list_field,INDEX=unsigned_int_input,VALUE=string_input),
    'ShowList': Block('data_showlist',LIST=list_field),
    'HideList': Block('data_hidelist',LIST=list_field),
}

reporter_blocks = {
    # Looks
    'BackdropNumberName': Block('looks_backdropnumbername',NUMBER_NAME=option_field(NumberNameOptions)).attach_option(NumberNameOptions),
    # Sensing
    'TouchingObject': TouchingObject().attach_option(TouchingObjectOptions),
    'TouchingColor': Block('sensing_touchingcolor',COLOR=color_input),
    'ColorIsTouchingColor': Block('sensing_coloristouchingcolor',COLOR=color_input,COLOR2=color_input),
    'AskAndWait': Block('sensing_askandwait',QUESTION=string_input),
    'Answer': MonitorableBlock('sensing_answer',sprite_specific=False),
    'KeyPressed': KeyPressed(),
    'MouseDown': Block('sensing_mousedown'),
    'MouseX': Block('sensing_mousex'),
    'MouseY': Block('sensing_mousey'),
    'Loudness': MonitorableBlock('sensing_loudness',sprite_specific=False),
    'Timer': MonitorableBlock('sensing_timer',sprite_specific=False),
    'Of': Of().attach_option(OfOptions),
    'Current': Current('sensing_current',CURRENTMENU=option_field(CurrentOptions)).attach_option(CurrentOptions),
    'DaysSince2000': Block('sensing_dayssince2000'),
    'Username': MonitorableBlock('sensing_username',sprite_specific=False),
    # Operator
    'Add': _operation('operator_add'),
    'Subtract': _operation('operator_subtract'),
    'Multiply': _operation('operator_multiply'),
    'Divide': _operation('operator_divide'),
    'Random': Block('operator_random',FROM=float_input,TO=float_input),
    'Equals': _comparison('operator_equals'),
    'Gt': _comparison('operator_gt'),
    'Lt': _comparison('operator_lt'),
    'And': _bool_operation('operator_and'),
    'Or': _bool_operation('operator_or'),
    'Not': Block('operator_not',OPERAND=bool_input),
    'Join': Block('operator_join',STRING1=string_input,STRING2=string_input),
    'LetterOf': Block('operator_letter_of',STRING=string_input,LETTER=unsigned_int_input),
    'Length': Block('operator_length',STRING=string_input),
    'Mod': _operation('operator_mod'),
    'Round': Block('operator_round',NUM=float_input),
    'MathOp': Block('operator_mathop',OPERATION=option_field(MathOpOptions),NUM=float_input).attach_option(MathOpOptions),
    # Data
    'Variable': Variable('data_variable',VARIABLE=variable_field),
    'List': List('data_list',LIST=list_field),
    'ItemOfList': Block('data_itemoflist',LIST=list_field,INDEX=unsigned_int_input),
    'ItemNumOfList': Block('data_itemnumoflist',LIST=list_field,ITEM=string_input),
    'LengthOfList': Block('data_lengthoflist',LIST=list_field),
    'ListContainsItem': Block('data_listcontainsitem',LIST=list_field,ITEM=string_input),
    # Arguments
    'ArgumentBoolean': Block('argument_reporter_boolean',VALUE=field),
    'ArgumentStringNumber': Block('argument_reporter_string_number',VALUE=field)
}

hat_blocks = {
    # Events
    'WhenFlagClicked': Block('event_whenflagclicked'),
    'WhenKeyPressed': Block('event_whenkeypressed',KEY_OPTION=option_field()),
    'WhenBackdropSwitchesTo': Block('event_whenbackdropswitchesto',BACKDROP=costume_field),
    'WhenGreaterThan': Block('event_whengreaterthan',WHENGREATERTHANMENU=option_field(WhenGreaterThanOptions),VALUE=unsigned_float_input)\
        .attach_option(WhenGreaterThanOptions),
    'WhenBroadcastReceived': Block('event_whenbroadcastreceived',BROADCAST_OPTION=message_field),
    
}

sprite_statement_blocks: dict[str,Block] = {
    **statement_blocks,
    # Motion
    'MoveSteps': Block('motion_movesteps',STEPS=float_input),
    'TurnRight': Block('motion_turnright',DEGREES=float_input),
    'TurnLeft': Block('motion_turnleft',DEGREES=float_input),
    'GoTo': GoTo().attach_option(GotoOptions),
    'GoToXY': Block('motion_gotoxy',X=float_input,Y=float_input),
    'GlideTo': GlideTo().attach_option(GotoOptions),
    'GlideToXY': Block('motion_glidetoxy',X=float_input,Y=float_input),
    'PointInDirection': Block('motion_pointindirection',DIRECTION=angle_input),
    'PointTowards': PointTowards().attach_option(GotoOptions),
    'ChangeXBy': Block('motion_changexby',DX=float_input),
    'SetX': Block('motion_setx',X=float_input),
    'ChangeYBy': Block('motion_changeyby',DY=float_input),
    'SetY': Block('motion_sety',Y=float_input),
    'SetRotationStyle': Block('motion_setrotationstyle',STYLE=option_field(SetRotationStyleOptions)).attach_option(SetRotationStyleOptions),
    'IfOnEdgeBounce': Block('motion_ifonedgebounce'),
    # Looks
    'SayForSecs': Block('looks_sayforsecs',MESSAGE=string_input,SECS=unsigned_float_input),
    'Say': Block('looks_say',MESSAGE=string_input),
    'ThinkForSecs': Block('looks_thinkforsecs',MESSAGE=string_input,SECS=unsigned_float_input),
    'Think': Block('looks_think',MESSAGE=string_input),
    'SwitchCostumeTo': SwitchCostumeTo(),
    'NextCostume': Block('looks_nextcostume'),
    'ChangeSizeBy': Block('looks_changesizeby',CHANGE=float_input),
    'SetSizeTo': Block('looks_setsizeto',SIZE=unsigned_float_input),
    'ChangeEffectBy': Block('looks_changeeffectby',EFFECT=option_field(EffectOptions),CHANGE=float_input).attach_option(EffectOptions),
    'SetEffectTo': Block('looks_seteffectto',EFFECT=option_field(EffectOptions),CHANGE=float_input).attach_option(EffectOptions),
    'ClearGraphicsEffect': Block('looks_cleargraphiceffects'),
    'Show': Block('looks_show'),
    'Hide': Block('looks_hide'),
    'GotoFrontBack': Block('looks_gotofrontback',FRONT_BACK=option_field(GoToFrontBackOptions))\
        .attach_option(GoForwardBackwardLayersOptions),
    'GoForwardBackwardLayers': Block('looks_goforwardbackwardlayers',FORWARD_BACKWARD=option_field(GoForwardBackwardLayersOptions),NUM=unsigned_int_input)\
        .attach_option(GoForwardBackwardLayersOptions)
}

sprite_reporter_blocks: dict[str,Block] = {
    **reporter_blocks,
    # Motion
    'XPosition': MonitorableBlock('motion_xposition',sprite_specific=True),
    'YPosition': MonitorableBlock('motion_yposition',sprite_specific=True),
    'Direction': MonitorableBlock('motion_direction',sprite_specific=True),
    # Looks
    'CostumeNumberName': Block('looks_costumenumbername',NUMBER_NAME=option_field(NumberNameOptions)).attach_option(NumberNameOptions),
    'Size': Block('looks_size'),
    # Sensing
    'DistanceTo': Block('sensing_distanceto',)
}

sprite_hat_blocks: dict[str,Block] = {
    **hat_blocks,
    # Event
    'WhenThisSpriteClicked': Block('event_whenthisspriteclicked'),
}

stage_statement_blocks: dict[str,Block] = {
    **statement_blocks,
    # Looks
    'SwitchBackdropToAndWait': SwitchBackdropToAndWait().attach_option(SwitchBackdropToOptions),
}

stage_reporter_blocks: dict[str,Block] = {
    **reporter_blocks,
}

stage_hat_blocks: dict[str,Block] = {
    **hat_blocks,
    # Event
    'WhenStageClicked': Block('event_whenstageclicked'),
}
